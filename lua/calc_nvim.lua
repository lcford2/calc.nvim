local M = {}

M.setup = function(config)
    -- Set up Python host to use the virtual environment
    local venv_path = vim.fn.stdpath("data") .. "/calc-nvim-venv"
    local python_path = venv_path .. "/bin/python"

    -- Only set python3_host_prog if the venv exists and hasn't been set by user
    if vim.fn.isdirectory(venv_path) == 1 and vim.fn.executable(python_path) ==
        1 then
        -- Only set if not already configured by user
        if vim.g.python3_host_prog == nil or vim.g.python3_host_prog == "" then
            vim.g.python3_host_prog = python_path
        end
    end

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
