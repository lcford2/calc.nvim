import vim
from asteval import Interpreter

def strings_to_ints(strings):
    return [int(i) for i in strings]

def get_selected_range():
    pos1 = strings_to_ints(vim.eval("getpos('v')"))
    pos2 = strings_to_ints(vim.eval("getpos('.')"))
    if pos1[1] >= pos2[1] and pos1[2] >= pos2[2]:
        return pos2, pos1
    else:
        return pos1, pos2

def get_text_from_range(start, stop):
    start_line, start_column = start[1], start[2]
    stop_line, stop_column = stop[1], stop[2]
    lines = vim.eval(f"nvim_buf_get_lines(0, {start_line - 1}, {stop_line}, v:false)")
    if len(lines) == 0:
        return ""
    elif len(lines) == 1:
        return lines[0][start_column - 1:stop_column]
    else:
        lines[0] = lines[0][start_column - 1:]
        lines[-1] = lines[-1][:stop_column]
        return "\n".join(lines)

def evaluate_expression(expr):
    aeval = Interpreter()
    try:
        value = float(aeval(expr))
    except Exception:
        value = expr
    return value

def replace_buffer_range(start, stop, replacement):
    s_buf, s_row, s_col, _ = start
    _, e_row, e_col, _ = stop
    set_text_args = [s_buf, s_row - 1, s_col - 1, e_row - 1, e_col, []]
    set_text_arg_string = ", ".join(str(i) for i in set_text_args)
    vim.eval(f"nvim_buf_set_text({set_text_arg_string})")
    set_text_args = [s_buf, s_row - 1, s_col - 1, s_row - 1, s_col - 1, [replacement]]
    set_text_arg_string = ", ".join(str(i) for i in set_text_args)
    vim.eval(f"nvim_buf_set_text({set_text_arg_string})")
    feedkeys = vim.eval("nvim_replace_termcodes('<esc>', v:true, v:false, v:true)")
    vim.eval(rf"nvim_feedkeys('{feedkeys}', 'x', v:false)")
    print(feedkeys)

def print_with_python():
    start, stop = get_selected_range()
    text = get_text_from_range(start, stop)
    result = evaluate_expression(text)
    replace_buffer_range(start, stop, f"{result:.4}")