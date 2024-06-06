"""Main module."""

import inspect
import logging
import os
import time
import traceback

from useful.connections import CloudLogger, FunctionError


def __get_current_micros():
    return int(time.time() * 1000000)


logger = None


def check(
    verbose=0,
):
    """
    Tracks the runtime of a function and sends email upon failure.

    Args:
        verbose (int, optional): The verbosity of the logging.

    Returns:
        The output of the underlying function.
    """
    logging.basicConfig(
        format="%(levelname)s:%(message)s",
        level=[logging.ERROR, logging.INFO, logging.DEBUG][verbose],
    )

    def decorate(func):
        """Decorate the function."""

        def useful_wrapper(*args, **kwargs):
            """Wrap the function."""
            global logger  # noqa: PLW0603
            if logger is None:
                logger = CloudLogger(api_key=os.environ.get("USEFUL_API_KEY"))
            # error handing
            try:
                started_at = __get_current_micros()
                return func(*args, **kwargs)
                finished_at = __get_current_micros()
                logging.info(f"[TIME] ended at: {finished_at}")
            except Exception as e:
                # [end] function log here
                payload = FunctionError(
                    function_name=func.__name__,
                    function_file=inspect.getfile(func),
                    started_at=started_at,
                    finished_at=__get_current_micros(),
                    error=traceback.format_exc(),
                )
                print(payload)
                logger.upload_error(payload)
                logger.wait()
                raise e  # noqa: TRY201

        return useful_wrapper

    return decorate
