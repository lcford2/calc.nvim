local luaxp = require("vim-calc.deps.luaxp")

local M = {}

local function calcExpr(expr)
  -- ---------------------------------------------------
  -- This function takes an expression and calculates the
  -- resulting value.
  -- ---------------------------------------------------
  -- compile parses the expression
  local parsedExp, cerr = luaxp.compile(expr)
  -- handle failures in parsing
  if parsedExp == nil then
    if cerr == nil then
      print("Parsing failed, cannot get error message.")
      return
    else
      print("Parsing failed: " .. cerr.message)
      return
    end
  end
  
  -- run calculates the expression
  local resultValue, rerr = luaxp.run(parsedExp)
  -- handle errors in calculation
  if resultValue == nil then
    if rerr == nil then
      print("Evaluation failed, cannot get error message.")
      return
    else
      print("Evaluation failed: " .. rerr.message)
      return
    end
  else
    return resultValue
  end
end

local function getSelectedRange()
  -- ---------------------------------------------------
  -- This function finds the current selected range in
  -- the buffer. It returns the start and end position 
  -- in order, even if the selection was made by 
  -- selecting backwards.
  -- ---------------------------------------------------
  -- get the selection positions
  local pos1 = vim.fn.getpos("v")
  local pos2 = vim.fn.getpos(".")
  -- order positions based on their relative values
  -- handles selecting forward and backwards
  if pos1[2] >= pos2[1] and pos1[3] >= pos2[3] then
    return pos2, pos1
  else
    return pos1, pos2
  end
end

local function getSelectedText()
  -- ---------------------------------------------------
  -- This function gets the currently selected text in
  -- visual mode. Can handle multiple lines.
  -- ---------------------------------------------------
  local select_start, select_stop = getSelectedRange()
  -- extract the start and end row and column
  local start_line, start_column = select_start[2], select_start[3]
  local stop_line, stop_column = select_stop[2], select_stop[3]
  -- get the lines of the buffer that are selected
  local lines = vim.api.nvim_buf_get_lines(0, start_line - 1, stop_line, false)
  
  -- handle no selection, single line, and multi line
  local text = ""
  if #lines == 0 then
    text = ""
  elseif #lines == 1 then
    text = string.sub(lines[1], start_column, stop_column)
  else
    lines[1] = string.sub(lines[1], start_column)
    lines[#lines] = string.sub(lines[#lines], 1, stop_column)
    text = table.concat(lines, "\n")
  end
  return text, select_start, select_stop
end

function M.calcSelectedText()
  -- ---------------------------------------------------
  -- This function retrieves the selected text from the
  -- buffer, uses luaxp to parse and calculate the 
  -- resulting value, and replaces the selected text
  -- with the resulting value.
  -- ---------------------------------------------------
  local text, select_start, select_stop = getSelectedText()
  local s_buf, s_row, s_col, _ = unpack(select_start)
  local _, e_row, e_col, _ = unpack(select_stop)
  local result = calcExpr(text)
  vim.api.nvim_buf_set_text(
    s_buf,
    s_row - 1,
    s_col - 1,
    e_row - 1,
    e_col,
    {}
  )
  vim.api.nvim_buf_set_text(
    s_buf,
    s_row - 1,
    s_col - 1,
    s_row - 1,
    s_col - 1,
    { string.format("%.4f", result) }
  )
  vim.api.nvim_feedkeys(
    vim.api.nvim_replace_termcodes(
      '<esc>',
      true,
      false,
      true),
    'x', false
  )
end

return M
