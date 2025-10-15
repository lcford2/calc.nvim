-- Build script for calc.nvim
-- Creates a virtual environment and installs Python dependencies
local function execute(cmd)
    local handle = io.popen(cmd .. " 2>&1")
    if not handle then
        error("Failed to execute command: " .. cmd)
        return nil
    end
    local result = handle:read("*a")
    local success = handle:close()
    return success, result
end

-- Determine the virtual environment path
local venv_path = vim.fn.stdpath("data") .. "/calc-nvim-venv"
local python_executable = venv_path .. "/bin/python"
local pip_executable = venv_path .. "/bin/pip"

-- Check if Python 3 is available
local python_cmd = "python3"
local success, _ = execute("which python3")
if not success then
    python_cmd = "python"
    success, _ = execute("which python")
    if not success then
        error("Python 3 is required but not found in PATH")
        return
    end
end

print("Creating virtual environment at: " .. venv_path)

-- Create virtual environment if it doesn't exist
if vim.fn.isdirectory(venv_path) == 0 then
    local venv_success, venv_output = execute(
                                          python_cmd .. " -m venv " .. venv_path)
    if not venv_success then
        error("Failed to create virtual environment:\n" ..
                  (venv_output or "Unknown error"))
        return
    end
    print("Virtual environment created successfully")
else
    print("Virtual environment already exists")
end

-- Upgrade pip
print("Upgrading pip...")
local pip_upgrade_success, pip_upgrade_output =
    execute(pip_executable .. " install --upgrade pip")
if not pip_upgrade_success then
    print("Warning: Failed to upgrade pip:\n" ..
              (pip_upgrade_output or "Unknown error"))
end

-- Install required packages
print("Installing pynvim and asteval...")
local install_success, install_output = execute(pip_executable ..
                                                    " install pynvim asteval")
if not install_success then
    error("Failed to install Python dependencies:\n" ..
              (install_output or "Unknown error"))
    return
end

print("Python dependencies installed successfully!")
print("\nNext steps:")
print("1. Run :UpdateRemotePlugins")
print("2. Restart Neovim")
print("3. Run :checkhealth calc_nvim to verify installation")
