"""Contains tools to connect to cloud services."""

import logging

import requests
from pydantic import BaseModel


class FunctionError(BaseModel):
    """A representation of a function error data."""

    function_name: str
    function_file: str
    started_at: int
    finished_at: int
    error: str


class CloudLogger:
    """A class to log data to the cloud."""

    def __init__(self, api_key, dev_mode=False):
        """Set the API and synchronization variables."""
        if api_key is None:
            raise RuntimeError(
                "Authentication needed. Generate a key at: "
                "https://usefulmachines.dev/"
            )

        self.api_key = api_key
        self.API_ENDPOINT = (
            "https://lite.api.usefulmachines.dev/dev/error"
            if dev_mode
            else "https://lite.api.usefulmachines.dev/dev/error"
        )

    def upload_error(self, data: FunctionError):
        """Upload a function error to the cloud."""
        logging.info(f"[Useful] Upload error called with data: {data}")
        requests.post(
            f"{self.API_ENDPOINT}",
            data=data.model_dump_json(exclude_none=True),
            headers={"x-api-key": self.api_key},
            timeout=3,
        )


class FakeCloudLogger:
    """A fake cloud logger that does nothing but uploads data to a list attribute."""

    def __init__(self):
        """Initialize the FakeCloudLogger."""
        self.all_data = []

    def upload_error(self, data):
        """Simulate an function error upload to the cloud."""
        logging.info(f"[Useful] Upload error called with data: {data}")
        self.all_data.append(data.model_dump_json(exclude_none=True))
