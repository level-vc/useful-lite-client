"""Test suite for the Useful class."""

from dotenv import load_dotenv

import useful

load_dotenv()


def test_error():
    """General error test."""

    @useful.check()
    def fail():
        raise ValueError("This is a test error.")

    worked = False
    try:
        fail()
    except ValueError:
        worked = True
    if not worked:
        raise RuntimeError("Test failed.")


if __name__ == "__main__":
    test_error()
    print("Test passed.")
