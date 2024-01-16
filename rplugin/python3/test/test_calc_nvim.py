from unittest.mock import MagicMock

import pytest

from ..calc_nvim import CalcNvim, strings_to_ints


# util funcs test
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


# plugin tests
@pytest.fixture
def nvim_mock():
    return MagicMock()


@pytest.fixture
def plugin(nvim_mock):
    return CalcNvim(nvim_mock)


def getpos_side_effect_normal_case(*args, **kwargs):
    if args == ("v",):
        return [0, 1, 4, 0]
    else:
        return [0, 1, 10, 0]


def getpos_side_effect_reversed_case(*args, **kwargs):
    if args == ("v",):
        return [0, 1, 10, 0]
    else:
        return [0, 1, 4, 0]


def getpos_side_effect_visual_line(*args, **kwargs):
    if args == ("v",):
        return [0, 1, 10, 0]
    else:
        return [0, 1, 10, 0]


def test_get_selected_range_normal_case(plugin, nvim_mock):
    nvim_mock.funcs.getpos.side_effect = getpos_side_effect_normal_case
    assert plugin.get_selected_range() == ([0, 1, 4, 0], [0, 1, 10, 0])


def test_get_selected_range_reversed_case(plugin, nvim_mock):
    nvim_mock.funcs.getpos.side_effect = getpos_side_effect_reversed_case
    assert plugin.get_selected_range() == ([0, 1, 4, 0], [0, 1, 10, 0])


def test_get_selected_range_visual_line(plugin, nvim_mock):
    nvim_mock.funcs.getpos.side_effect = getpos_side_effect_visual_line
    text = "this is a line"
    nvim_mock.api.buf_get_lines.return_value = [text]
    assert plugin.get_selected_range() == ([0, 1, 1, 0], [0, 1, len(text), 0])
