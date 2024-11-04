import unittest
import numpy
import task


class TestTask(unittest.TestCase):
    def test(self):
        t = task.Task()
        t.work()
        numpy.testing.assert_allclose(numpy.dot(t.a, t.x), t.b)


if __name__ == "__main__":
    unittest.main()
