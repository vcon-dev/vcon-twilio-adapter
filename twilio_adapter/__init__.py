"""Twilio adapter - backwards compatibility layer.

This module re-exports from the new adapters.twilio package for
backward compatibility with existing code that imports from twilio_adapter.
"""

__version__ = "0.1.0"

# Re-export from new location for backwards compatibility
from adapters.twilio.config import TwilioConfig as Config
from adapters.twilio.builder import TwilioRecordingData, TwilioVconBuilder as VconBuilder
from adapters.twilio.webhook import create_app

# Also export core modules that were previously in this package
from core.poster import HttpPoster
from core.tracker import StateTracker

__all__ = [
    "Config",
    "TwilioRecordingData",
    "VconBuilder",
    "HttpPoster",
    "StateTracker",
    "create_app",
]
