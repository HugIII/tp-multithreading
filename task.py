"""
====================================================================
File: task.py
Author: Baffogne Clara, Blayes Hugo
Date: 06/12/24
Description:
    This file defines the `Task` class, which represents a computational problem 
    involving solving a linear system of equations. The class includes methods 
    for generating problem inputs, performing computations, and serializing 
    or deserializing tasks in JSON format.

Usage:
    python task.py

Version: 1.0.0
====================================================================
"""

import time
import json
import numpy as np


class Task:
    def __init__(self, identifier=0, size=None, time=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.random.rand(self.size)
        self.time = time or 0

    def work(self):
        # Solve the linear system Ax = b and measure the execution time.
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start
        return self.x

    def to_json(self) -> str:
        # Convert the task instance to a JSON string.
        return json.JSONEncoder().encode(
            {
                "a": self.a.tolist(),
                "b": self.b.tolist(),
                "x": self.x.tolist(),
                "identifier": self.identifier,
                "time": self.time,
                "size": self.size,
            }
        )

    @staticmethod
    def from_json(text: str) -> "Task":
        # Recreate a Task instance from a JSON string (input text).
        d = json.loads(text)
        t = Task(int(d["identifier"]), int(d["size"]), float(d["time"]))
        t.a = np.array(d["a"], np.float64)
        t.b = np.array(d["b"], np.float64)
        t.x = np.array(d["x"], np.float64)
        return t

    def __eq__(self, other: "Task") -> bool:
        # Define equality between Task instances (inputs self and other) based on all attributes.
        return (
            (self.a == other.a).all()
            and (self.b == other.b).all()
            and (self.x == other.x).all()
            and self.identifier == other.identifier
            and self.time == other.time
            and self.size == other.size
        )
