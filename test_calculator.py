import pytest
from calculator import add, subtract

def test_add():
    """Test the add function with various inputs"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0

def test_subtract():
    """Test the subtract function with various inputs"""
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5
    assert subtract(3.5, 1.5) == 2.0 