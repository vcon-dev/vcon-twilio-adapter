#!/usr/bin/env python3
"""Main entry point for vCon telephony adapters.

Supports running individual adapters via command line argument:
    python main.py twilio    # Run Twilio adapter
    python main.py           # Default: Run Twilio adapter
"""

import sys
import logging
import uvicorn


def setup_logging(level: str = "INFO"):
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def run_twilio_adapter():
    """Run the Twilio adapter."""
    from adapters.twilio import TwilioConfig, create_app

    # Load configuration
    config = TwilioConfig()

    # Setup logging
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)

    logger.info("Starting vCon Twilio Adapter...")
    logger.info(f"Conserver URL: {config.conserver_url}")
    logger.info(f"Twilio signature validation: {config.validate_twilio_signature}")
    logger.info(f"Download recordings: {config.download_recordings}")
    logger.info(f"Recording format: {config.recording_format}")

    # Create FastAPI app
    app = create_app(config)

    # Run server
    logger.info(f"Starting server on {config.host}:{config.port}")
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level.lower()
    )


# Registry of available adapters
ADAPTERS = {
    "twilio": run_twilio_adapter,
    # Future adapters will be added here:
    # "freeswitch": run_freeswitch_adapter,
    # "asterisk": run_asterisk_adapter,
    # "telnyx": run_telnyx_adapter,
    # "bandwidth": run_bandwidth_adapter,
}


def main():
    """Main entry point."""
    try:
        # Get adapter name from command line (default to twilio)
        adapter_name = sys.argv[1] if len(sys.argv) > 1 else "twilio"

        if adapter_name in ("--help", "-h"):
            print("Usage: vcon-adapter [ADAPTER_NAME]")
            print(f"\nAvailable adapters: {', '.join(ADAPTERS.keys())}")
            print("\nDefault: twilio")
            sys.exit(0)

        if adapter_name not in ADAPTERS:
            print(f"Unknown adapter: {adapter_name}", file=sys.stderr)
            print(f"Available adapters: {', '.join(ADAPTERS.keys())}", file=sys.stderr)
            sys.exit(1)

        # Run the selected adapter
        ADAPTERS[adapter_name]()

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
