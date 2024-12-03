import unittest
import numpy
import task


class TestTask(unittest.TestCase):
    def test(self):
    	size = np.random.randint(300, 3_000)
	a = np.random.rand(size, size)
        b = np.random.rand(size)
        t = task.Task(a,b)
        t.work()
        numpy.testing.assert_allclose(numpy.dot(t.a, t.x), t.b)


if __name__ == "__main__":
    unittest.main()
