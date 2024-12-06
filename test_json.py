"""
====================================================================
File: test_json.py
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    Test whether the transformation of the task into a json, the json into a task and the comparison between tasks work properly

Usage:
    python test_json.py

Local dependencies:
        - task (task.py)

Dependencies:
        - unittest

Version: 1.0.0
====================================================================
"""

import unittest
import task


class TestJson(unittest.TestCase):
    def test(self):
        a = task.Task()

        # create json from task a
        txt = a.to_json()

        # create task b from json
        b = task.Task.from_json(txt)

        # logically a and b are the same
        assert a == b


if __name__ == "__main__":
    unittest.main()
