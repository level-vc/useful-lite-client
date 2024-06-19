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
            except Exception as e:
                tb_lines = traceback.format_exc().splitlines()
                print(tb_lines)

                filtered_tb = [
                    line
                    for line in tb_lines
                    if "useful_wrapper" not in line
                    and "return func(*args, **kwargs)" not in line
                ]
                final_traceback = "\n".join(filtered_tb)
                # [end] function log here
                payload = FunctionError(
                    function_name=func.__name__,
                    function_file=inspect.getfile(func),
                    started_at=started_at,
                    finished_at=__get_current_micros(),
                    error=final_traceback,
                )
                print(payload)
                logger.upload_error(payload)
                raise e  # noqa: TRY201

        return useful_wrapper

    return decorate
