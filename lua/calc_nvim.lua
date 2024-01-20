local M = {}

M.setup = function(config)
    -- call setup function of python plugin
    vim.api.nvim_call_function("CalcNvimSetup", {config})
end

M.calculate = function(...)
    -- call the calculate function from python plugin
    vim.api.nvim_call_function("CalcNvimCalculate", {...})
end

M.format_number = function(...)
    -- call the format function from python plugin
    vim.api.nvim_call_function("CalcNvimFormatNumber", {...})
end

return M
