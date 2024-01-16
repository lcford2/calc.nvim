import neovim
import pytest
from unittest.mock import MagicMock, create_autospec
from ..calc_nvim import CalcNvim

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
