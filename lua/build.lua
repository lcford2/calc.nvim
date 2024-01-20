vim.cmd("UpdateRemotePlugins")

-- Install python deps
if os.execute("which pip") then
    os.execute("pip install pynvim asteval")
else
    error("Cannot find pip to install pynvim and asteval.")
end
