"""Docstring."""
import unittest

from src import SingleCircuit


class TestSingleCircuit(unittest.TestCase):
    """Tests Impl class implementation."""

    def test_x_gate(self):
        """Tests run method implementation."""
        main = SingleCircuit()
        main.x_gate()
        main.measure()
        self.assertEqual(main.create_job(), {'1': 1000})
