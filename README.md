## vimcalc: A Calculator in Vim

Inspired by (vim-calc)[https://github.com/theniceboy/vim-calc].

Uses (asteval)[https://newville.github.io/asteval/] to perform *safe-ish* 
expression evaluations and replaces the expression right in your buffer!


#### Introduction
`vimcalc` is a fully functional calculator that will replace expressions in your buffer
with their result!

![Demo](demo.gif)


#### Usage - NOTREADY
Do **`:call Calc()`** inside vim to calculate the math equation in the current line (`vim-calc` will tell you if there's any error in terms of the equation within the current line)

Or, if you want a key-binding, add this to your `vimrc`/`init.vim`:

```vim
nnoremap <LEADER>a :call Calc()<CR>
```

Now, you can press `LEADER` and `a` to calculate!

#### Installation - NOTREADY
Install `vim-calc` with [Lazy](https://github.com/folke/lazy.nvim):
```lua
require("lazy").setup({
    "lcford2/vim-calc",
})
```

#### License
MIT
