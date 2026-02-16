"""Twilio-specific configuration extending base config."""

import os
from typing import Optional

from core.base_config import BaseConfig


class TwilioConfig(BaseConfig):
    """Twilio adapter configuration with platform-specific settings."""

    def __init__(self, env_file: Optional[str] = None):
        """Load configuration from .env file.

        Args:
            env_file: Optional path to .env file
        """
        super().__init__(env_file)

        # Override default state file name
        self.state_file = os.getenv("STATE_FILE", ".twilio_adapter_state.json")

        # Twilio-specific settings
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.validate_twilio_signature = os.getenv(
            "VALIDATE_TWILIO_SIGNATURE", "true"
        ).lower() in ("true", "1", "yes")

        if self.validate_twilio_signature and not self.twilio_auth_token:
            raise ValueError(
                "TWILIO_AUTH_TOKEN is required when VALIDATE_TWILIO_SIGNATURE is true"
            )

        # Webhook URL for signature validation (optional, can be auto-detected)
        self.webhook_url = os.getenv("WEBHOOK_URL")

    def get_twilio_auth(self) -> Optional[tuple]:
        """Get Twilio authentication tuple for API requests."""
        if self.twilio_account_sid and self.twilio_auth_token:
            return (self.twilio_account_sid, self.twilio_auth_token)
        return None
