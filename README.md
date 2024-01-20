# calc.nvim: A Calculator in NeoVim

Inspired by [vim-calc](https://github.com/theniceboy/vim-calc).

Uses [asteval](https://newville.github.io/asteval/) to perform *safe-ish* 
expression evaluations and replaces the expression right in your buffer!


## Introduction

`calc.nvim` is a fully functional calculator that will replace expressions in your buffer
with their result!

![Demo](demo.gif)

## Dependencies

`calc.nvim` uses Python for evaluation. It is assumed that Python 3.8 to 3.11 is installed on your system.

To communicate with Neovim using python, the [`pynvim`](https://pynvim.readthedocs.io/en/latest/installation.html) Python package must also be installed.

All expression evaluation is performed by the Python package [`asteval`](https://newville.github.io/asteval/).

Some plugin managers will attempt to install these packages using `pip` when `calc.nvim` is first installed; however, they can be installed directly with `pip`.

Additionally, to take full advantage of the capabilities of `asteval`, the `numpy` and `numpy_financial` packages can be installed with `pip` as well.

## Installation

Install `vimcalc` with [Lazy](https://github.com/folke/lazy.nvim):

```lua
require("lazy").setup({
    "lcford2/calc.nvim"
})
```

## Usage

To bind to a key and set the float format of the expression,
add this to your `nvim` configuration:

```lua
local calc = require("calc_nvim")

calc.setup({
  float_format="0.3",
})
vim.keymap.set("v", "<C-c>", calc.calculate, {})
```

Now, you can press `Control` and `c` to calculate!
