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

To install all of these dependencies to your Python3 environment, you can use the following command:

```shell
pip install pynvim asteval numpy numpy_financial
```

## Installation

### Automatic Installation with Lazy.nvim (Recommended)

Install `calc.nvim` with [Lazy](https://github.com/folke/lazy.nvim), which will automatically handle Python dependencies:

```lua
require("lazy").setup({
    {
        "lcford2/calc.nvim",
        build = ":lua require('build')",
    }
})
```

When you install the plugin, Lazy.nvim will:
1. Create a dedicated Python virtual environment
2. Install `pynvim` and `asteval` packages automatically
3. Run `:UpdateRemotePlugins` to register the Python plugin

After installation:
1. Restart Neovim
2. Run `:checkhealth calc_nvim` to verify everything is working

### Manual Installation

If you prefer to manage Python dependencies yourself:

1. Install the required Python packages:
   ```shell
   pip install pynvim asteval
   ```

2. Install the plugin with your package manager:
   ```lua
   require("lazy").setup({
       "lcford2/calc.nvim"
   })
   ```

3. Run `:UpdateRemotePlugins` and restart Neovim

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
