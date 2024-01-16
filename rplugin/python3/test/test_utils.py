import pytest

from ..utils import strings_to_ints

def test_strings_to_ints_valid():
    strings = ["4", "5", "2", "1"]
    ints = [4, 5, 2, 1]
    assert strings_to_ints(strings) == ints

def test_strings_to_ints_with_float_string():
    strings = ["4", "5", "2.1", "1"]
    with pytest.raises(ValueError) as excinfo:
        strings_to_ints(strings)
    assert "invalid literal for int() with base 10: '2.1'" in str(excinfo.value)

def test_strings_to_ints_with_list():
    with pytest.raises(TypeError) as excinfo:
        strings_to_ints([[]])
    assert "int() argument must be a string" in str(excinfo.value)

