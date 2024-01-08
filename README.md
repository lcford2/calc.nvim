## vim-calc: A Calculator in Vim

Forked from (vim-calc)[https://github.com/theniceboy/vim-calc] with the goal of
adding custom functionality for evaluating and replacing selected
text in a buffer.


#### Introduction
`vim-calc` is a fully functional calculator that you might feel missing in `Vim`.

![Demo](demo.gif)


#### Usage
Do **`:call Calc()`** inside vim to calculate the math equation in the current line (`vim-calc` will tell you if there's any error in terms of the equation within the current line)

Or, if you want a key-binding, add this to your `vimrc`/`init.vim`:

```vim
nnoremap <LEADER>a :call Calc()<CR>
```

Now, you can press `LEADER` and `a` to calculate!

#### Installation
Install `vim-calc` with [Lazy](https://github.com/folke/lazy.nvim):
```lua
require("lazy").setup({
    "lcford2/vim-calc",
})
```

#### Todos
- [ ] Convert equation to `latex` form

#### License
MIT
