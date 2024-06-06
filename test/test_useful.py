"""Test suite for the Useful class."""

import useful


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
