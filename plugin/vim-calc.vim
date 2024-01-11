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

if !has('python3')
    echomsg ":python3 is not available, vimcalc will not be loaded"
    finish
endif

python3 import vimcalc.vimcalc

command! Calculate python3 vimcalc.vimcalc.calculate()
