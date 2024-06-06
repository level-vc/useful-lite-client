"""Contains tools to connect to cloud services."""

import asyncio
import concurrent
import logging
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool

import nest_asyncio
import requests
from pydantic import BaseModel


class FunctionError(BaseModel):
    """A representation of a function error data."""

    function_name: str
    function_file: str
    started_at: int
    finished_at: int
    error: str


# Enable multithreading inside multithreading like IPython kernel and parallel tasks
nest_asyncio.apply()


class CloudLogger:
    """A class to log data to the cloud."""

    MAX_CONCURRENCY = 10

    def __init__(self, api_key, dev_mode=False):
        """Set the API and synchronization variables."""
        if api_key is None:
            raise RuntimeError(
                "Authentication needed. Generate a key at: "
                "https://usefulmachines.dev/"
            )

        self.api_key = api_key
        self.tasks = []
        self.API_ENDPOINT = (
            "https://8o2881lhg6.execute-api.us-east-2.amazonaws.com/prod"
            if dev_mode
            else "https://8o2881lhg6.execute-api.us-east-2.amazonaws.com/prod"
        )

    def upload_task(self, endpoint, data):
        """Uploads data to endpoints synchronously."""
        requests.post(
            f"{self.API_ENDPOINT}{endpoint}",
            data=data,
            headers={"x-api-key": self.api_key},
            timeout=3,
        )

    async def __wait_async(self):
        """Wait for all tasks to finish asynchronously."""
        with ProcessPoolExecutor(max_workers=self.MAX_CONCURRENCY) as executor:
            try:
                futures = [executor.submit(self.upload_task, *x) for x in self.tasks]
                [concurrent.futures.as_completed(x) for x in futures]
                self.tasks = []

            except BrokenProcessPool:
                # If process pool breaks, reset request handling queue
                logging.warning("Failed to execute requests")
                self.tasks = []
                pass

    def wait(self):
        """Wait for all tasks to finish."""
        asyncio.run(self.__wait_async())

    def upload_error(self, data: FunctionError):
        """Upload a function error to the cloud."""
        logging.info(f"[Useful] Upload error called with data: {data}")
        self.tasks.append(("/error", data.model_dump_json(exclude_none=True)))


class FakeCloudLogger:
    """A fake cloud logger that does nothing but uploads data to a list attribute."""

    def __init__(self):
        """Initialize the FakeCloudLogger."""
        self.all_data = []

    def wait(self):
        """Simulate a wait."""
        pass

    def upload_error(self, data):
        """Simulate an function error upload to the cloud."""
        logging.info(f"[Useful] Upload error called with data: {data}")
        self.all_data.append(data.model_dump_json(exclude_none=True))
