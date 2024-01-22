local M = {}

M.setup = function(config)
    -- call setup function of python plugin
    vim.api.nvim_call_function("CalcNvimSetup", {config})
end

M.calculate = function(...)
    -- evaluate the selected expression and replace the
    -- selection with the result
    vim.api.nvim_call_function("CalcNvimCalculate", {...})
end

M.format_number = function(format)
    -- format a selected number, if format is not given
    -- the default format specified during setup will be
    -- used
    vim.api.nvim_call_function("CalcNvimFormatNumber", {format})
end

M.set_format = function(format)
    -- Set the format of the calculator
    -- can be used to change the desired format 
    -- of the calculator on the fly
    if type(format) == "string" then
        vim.api.nvim_call_function("CalcNvimSetFormat", {format})
    end
end

return M

