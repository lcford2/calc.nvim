" Title:        calc.nvim
" Description:  A plugin to calculate math in a buffer
" Last Change:  Jan 11th 2023
" Maintainer:   Lucas Ford

" Prevents the plugin from being loaded multiple times. If the loaded
" variable exists, do nothing more. Otherwise, assign the loaded
" variable and continue running this instance of the plugin.
if exists("g:loaded_calcnvim")
    finish
endif
let g:loaded_calcnvim = 1

if !has('python3')
    echomsg ":python3 is not available, calc.nvim will not be loaded"
    finish
endif

python3 import calc_nvim.calc_nvim

command! Calculate python3 calc_nvim.calc_nvim.calculate()
