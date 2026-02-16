"""Base configuration management for telephony adapters."""

import os

from dotenv import load_dotenv


class BaseConfig:
    """Base configuration class with common settings for all adapters.

    Subclasses should extend this to add platform-specific settings.
    """

    def __init__(self, env_file: str | None = None):
        """Load configuration from .env file.

        Args:
            env_file: Optional path to .env file
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        # Server settings
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8080"))

        # Conserver settings (required)
        self.conserver_url = os.getenv("CONSERVER_URL")
        if not self.conserver_url:
            raise ValueError("CONSERVER_URL environment variable is required")

        # Optional conserver authentication
        self.conserver_api_token = os.getenv("CONSERVER_API_TOKEN")
        self.conserver_header_name = os.getenv("CONSERVER_HEADER_NAME", "x-conserver-api-token")

        # State tracking
        self.state_file = os.getenv("STATE_FILE", ".adapter_state.json")

        # Ingress lists for vCon routing
        ingress_lists_str = os.getenv("INGRESS_LISTS", "")
        self.ingress_lists: list[str] = [
            item.strip() for item in ingress_lists_str.split(",") if item.strip()
        ]

        # Recording download settings
        self.download_recordings = os.getenv("DOWNLOAD_RECORDINGS", "true").lower() in (
            "true",
            "1",
            "yes",
        )

        # Recording format preference (wav or mp3)
        self.recording_format = os.getenv("RECORDING_FORMAT", "wav").lower()
        if self.recording_format not in ("wav", "mp3"):
            raise ValueError(
                f"RECORDING_FORMAT must be 'wav' or 'mp3', got: {self.recording_format}"
            )

        # Logging level
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    def get_headers(self) -> dict[str, str]:
        """Get HTTP headers for conserver requests."""
        headers = {"Content-Type": "application/json"}
        if self.conserver_api_token:
            headers[self.conserver_header_name] = self.conserver_api_token
        return headers
