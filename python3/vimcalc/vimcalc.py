import vim
from datetime import datetime
from asteval import Interpreter

def get_timestamp(dt=None):
    """Get the isoformatted timestamp

    If dt is not provided, will return the current time.

    Args:
        dt (datetime, optional): A datetime to convert to isoformat
    """
    if dt:
        return datetime.isoformat(dt)
    else:
        return datetime.isoformat(datetime.now())

def log(level: str, message: str):
    """Log a message to neovim

    Args:
        level (str): Level to log message
        message (str): Message to log
    """
    ts = get_timestamp()
    output = f"[{level.upper()}] [vimcalc] [{ts}] : {message}"
    print(output)

def strings_to_ints(strings: list[str]) -> list[int]:
    """Convert a list of strings to a list of integers

    Args:
        strings (list[str]): List of strings that can be converted to integers

    Returns:
        list[int]: List of integers from the strings provided
    """
    return [int(i) for i in strings]

def get_selected_range() -> tuple[list[int], list[int]]:
    """Get the currenly selected range from the buffer

    Returns:
        tuple[list[int], list[int]]: The first position and second position of the
            selected range
    """
    pos1 = strings_to_ints(vim.eval("getpos('v')"))
    pos2 = strings_to_ints(vim.eval("getpos('.')"))
    log("debug", f"pos1 = {pos1}; pos1 = {pos2}")
    if pos1[1] >= pos2[1] and pos1[2] >= pos2[2]:
        return pos2, pos1
    else:
        return pos1, pos2

def get_text_from_range(start: list[int], stop: list[int]) -> str:
    """Extrac the text from a buffer given a start and stop position

    Args:
        start (list[int]): The start position of the selection
        stop (list[int]): The stop position of the selection

    Returns:
        str: The selected text in the buffer
    """
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

def preprocess_input(text: str) -> str:
    """Preprocess the text from the buffer before evaluation

    Args:
        text (str): Raw test from buffer

    Returns:
        str: Expression to be evaluated
    """
    return text.lstrip(" ").rstrip(" ") 

def evaluate_expression(expr: str) -> float | str:
    """Use asteval to evaluate the math expression

    Args:
        expr (str): Expression to be evaluated

    Returns:
        float | str: Result of the evaluation or the provided input on error
    """
    aeval = Interpreter()
    try:
        value = float(aeval(expr))
    except Exception:
        value = expr
    return value

def replace_buffer_range(start: list[int], stop: list[int], replacement: str):
    """Replace text in a buffer

    Args:
        start (list[int]): Start position of the text to replace 
        stop (list[int]): Stop position of the text to replace
        replacement (str): String to replace the current text with
    """
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

def calculate():
    """Entrypoint to the plugin.

    Will extract the text from the currently selected range, 
    evaluate it, and then replace the currently selected range with the result.

    """
    start, stop = get_selected_range()
    text = get_text_from_range(start, stop)
    log("debug", f"Selected text: {text}")
    expr = preprocess_input(text)
    log("debug", f"Preprocessed text: {expr}")
    result = evaluate_expression(expr)
    log("debug", f"Result: {result}")
    if isinstance(result, float):
        output = f"{result:.4}"
    else:
        output = result
    replace_buffer_range(start, stop, output)
