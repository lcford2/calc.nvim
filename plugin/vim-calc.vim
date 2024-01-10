" Title:        vim-calc
" Description:  A plugin to calculate math in a buffer
" Last Change:  Jan 8th 2023
" Maintainer:   Lucas Ford

" Prevents the plugin from being loaded multiple times. If the loaded
" variable exists, do nothing more. Otherwise, assign the loaded
" variable and continue running this instance of the plugin.
if exists("g:loaded_vimcalc")
    finish
endif
let g:loaded_vimcalc = 1

" Defines a package path for Lua. This facilitates importing the
" Lua modules from the plugin's dependency directory.
let s:vimcalc_deps_loc =  expand("<sfile>:h:r") . "/../lua/vim-calc/deps"
exe "lua package.path = package.path .. ';" . s:vimcalc_deps_loc . "/lua-?/init.lua'"

" Exposes the plugin's functions for use as commands in Neovim.
command! -nargs=0 CalcSelectedText lua require("vim-calc").CalcSelectedText()

