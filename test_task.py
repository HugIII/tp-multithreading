import unittest
import task
import numpy as np


class TestTask(unittest.TestCase):
    def test(self):
        t = task.Task()
        t.work()
        np.testing.assert_allclose(np.dot(t.a, t.x), t.b)


if __name__ == "__main__":
    unittest.main()
