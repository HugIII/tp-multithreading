import unittest
import numpy as np
import task


class TestJson(unittest.TestCase):
    def test(self):
        a = task.Task()
        txt = a.to_json()
        b = task.Task.from_json(txt)
        assert a == b


if __name__ == "__main__":
    unittest.main()
