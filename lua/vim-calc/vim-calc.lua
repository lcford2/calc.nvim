local luaxp = require("luaxp")

local M = {}

function M.Calc(expr)
  local parsedExp, cerr = luaxp.compile(expr)
  if parsedExp == nil then
    error("Parsing failed: " .. cerr.message)
  end

  local resultValue, rerr = luaxp.run(parsedExp)
  if resultValue == nil then
    error("Evaluation failed: " .. rerr.message)
  else
    print("Result: ", luaxp.isNull(resultValue) and "NULL" or tostring(resultValue))
  end
end

function M.GetSelectedText()
  local select_start = vim.fn.getpos("'<")
  local select_stop = vim.fn.getpos("'>")
  local line_start = select_start[2]
  local line_stop = select_stop[2]
  local text = vim.fn.getline(line_start, line_stop)
  print(text)
  return text
end
