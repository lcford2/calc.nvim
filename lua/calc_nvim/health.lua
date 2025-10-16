local M = {}

function M.check()
    vim.health.start("calc.nvim")

    local venv_path = vim.fn.stdpath("data") .. "/calc-nvim-venv"
    local python_path = venv_path .. "/bin/python"

    -- Check if virtual environment exists
    if vim.fn.isdirectory(venv_path) == 0 then
        vim.health.error("Virtual environment not found at: " .. venv_path, {
            "Run :Lazy build calc.nvim to create the virtual environment and install dependencies"
        })
        return
    end

    vim.health.ok("Virtual environment found at: " .. venv_path)

    -- Check if Python executable exists in venv
    if vim.fn.executable(python_path) == 0 then
        vim.health.error("Python executable not found in venv", {
            "The virtual environment may be corrupted. Try removing " ..
                venv_path .. " and running :Lazy build calc.nvim"
        })
        return
    end

    vim.health.ok("Python executable found: " .. python_path)

    -- Check if required Python packages are installed
    local check = vim.fn.system(python_path ..
                                    " -c 'import pynvim, asteval' 2>&1")
    if vim.v.shell_error ~= 0 then
        vim.health.error("Required Python packages not installed", {
            "Run :Lazy build calc.nvim to install pynvim and asteval",
            "Error: " .. check
        })
        return
    end

    vim.health.ok("Required Python packages installed (pynvim, asteval)")

    -- Check if plugin is registered with UpdateRemotePlugins
    local rplugin_manifest = vim.fn.stdpath("data") .. "/rplugin.vim"
    if vim.fn.filereadable(rplugin_manifest) == 1 then
        local manifest_content = vim.fn.readfile(rplugin_manifest)
        local calc_nvim_registered = false
        for _, line in ipairs(manifest_content) do
            if string.match(line, "calc[_-]nvim") or
                string.match(line, "calc%.nvim") then
                calc_nvim_registered = true
                break
            end
        end

        if calc_nvim_registered then
            vim.health.ok("Plugin registered with UpdateRemotePlugins")
        else
            vim.health.warn("Plugin not found in remote plugin manifest", {
                "Run :UpdateRemotePlugins and restart Neovim to register the plugin",
                "This is required for the plugin commands to work"
            })
        end
    else
        vim.health.warn("Remote plugin manifest not found", {
            "Run :UpdateRemotePlugins and restart Neovim to create the manifest",
            "This is required for the plugin commands to work"
        })
    end

    -- Check if python3_host_prog is set correctly
    if vim.g.python3_host_prog then
        if vim.g.python3_host_prog == python_path then
            vim.health.ok("python3_host_prog is set to calc.nvim venv")
        else
            vim.health.warn("python3_host_prog is set to: " ..
                                vim.g.python3_host_prog, {
                "This is fine if you have pynvim installed in that Python environment",
                "Otherwise, consider unsetting python3_host_prog to use the calc.nvim venv"
            })
        end
    else
        vim.health.info(
            "python3_host_prog not set, will be set automatically when setup() is called")
    end

    vim.health.ok("calc.nvim is properly configured!")
end

return M
