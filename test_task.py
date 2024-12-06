"""
====================================================================
File: test_task.py
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    Test if task resolution is successful

Usage:
    python test_task.py

Local dependencies:
        - task (task.py)

Dependencies:
        - unittest
        - numpy

Version: 1.0.0
====================================================================
"""

import unittest
import task
import numpy as np


class TestTask(unittest.TestCase):
    def test(self):
        t = task.Task()
        # work solves the equation Ax = B in which x is unconditional (A is a matrix and B a vector)
        t.work()
        # If work has worked, then A*x must be equal to B, which is what we're looking for in work
        np.testing.assert_allclose(np.dot(t.a, t.x), t.b)


if __name__ == "__main__":
    unittest.main()
