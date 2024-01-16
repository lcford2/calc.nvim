from datetime import datetime

import pynvim
from asteval import Interpreter
from .utils import LogLevel, strings_to_ints, get_timestamp


@pynvim.plugin
class CalcNvim:
    """Neovim plugin to evaluate expressions and replace them with the result."""

    NAME = "calc.nvim"

    def __init__(self, nvim):
        self.__nvim = nvim
        self.__aeval = Interpreter()
        self.__float_format = "0.3f"
        self.__init_time = get_timestamp()
        self.__log_level = LogLevel.FATAL

    @pynvim.function("CalcNvimSetup")
    def setup(self, args: list[dict]):
        """Setup function called by user to configure calc.nvim.

        Args:
            args (list[dict]): Arguments to parse for setting up the plugin.
        """
        # if setup args are provided, parse them
        if args and isinstance(args[0], dict):
            config = args[0]
            self.__float_format = config.get("float_format", self.__float_format)
            self.__log(LogLevel.DEBUG, f"Using float_format: {self.__float_format}")
            log_level = config.get("log_level", self.__log_level.name)
            # log level must be a valid member of the LogLevel enum
            if log_level.upper() in LogLevel.__members__:
                self.__log_level = LogLevel[log_level]
                self.__log(LogLevel.DEBUG, f"Using log_level: {self.__log_level.name}")
            else:
                self.__log(
                    LogLevel.ERROR,
                    f"Invalid log_level specified. Using {self.__log_level.name}.",
                )
        else:
            self.__log(LogLevel.ERROR, "Invalid configuration.")

    def __log(self, level: LogLevel, message: str):
        """Log a message to neovim.

        Args:
            level (LogLevel): Level to log message
            message (str): Message to log
        """
        ts = get_timestamp()
        output = f"[{level.name}] [{self.NAME}] [{ts}]: {message}\n"

        with open(f"/tmp/{self.NAME}.log", "a") as f:
            f.write(output)

        if level >= self.__log_level:
            if level >= LogLevel.WARN:
                self.__nvim.err_write(output)
            else:
                self.__nvim.out_write(output)

    def get_selected_range(self) -> tuple[list[int], list[int]]:
        """Get the currenly selected range from the buffer.

        Returns:
            tuple[list[int], list[int]]: The first position and second position of the
                selected range
        """
        pos1 = strings_to_ints(self.__nvim.funcs.getpos("v"))
        pos2 = strings_to_ints(self.__nvim.funcs.getpos("."))
        self.__log(LogLevel.DEBUG, f"pos1 = {pos1}; pos2 = {pos2}")
        # when in visual line mode, pos1 and pos2 should be equal
        if pos1 == pos2:
            # get the current line length
            lines = self.__nvim.api.buf_get_lines(0, pos1[1] - 1, pos1[1], False)
            try:
                # make sure plugin does not crash because len(lines) == 0
                line_length = len(lines[0])
                self.__log(LogLevel.DEBUG, "Positions equal, using entire line.")
                pos1[2] = 1
                pos2[2] = line_length
                self.__log(LogLevel.DEBUG, f"pos1 = {pos1}; pos2 = {pos2}")
                return pos1, pos2
            except IndexError:
                # inform that there was an error getting currently selected range
                self.__log(
                    LogLevel.FATAL,
                    f"Could not determine selected range: {pos1}, {pos2}",
                )
                return [], []

        if pos1[1] >= pos2[1] and pos1[2] >= pos2[2]:
            # the text was selected from left to right, so the cursor
            # position is less than the start of selection position
            self.__log(LogLevel.DEBUG, "pos2 > pos1, swapping.")
            return pos2, pos1
        else:
            # normal behavior, text was selected from left to right
            # in visual mode
            return pos1, pos2

    def get_text_from_range(self, start: list[int], stop: list[int]) -> str:
        """Extract the text from a buffer given a start and stop position.

        Args:
            start (list[int]): The start position of the selection
            stop (list[int]): The stop position of the selection

        Returns:
            str: The selected text in the buffer
        """
        start_line, start_column = start[1], start[2]
        stop_line, stop_column = stop[1], stop[2]
        # retrieve the text selected in the current buffer
        lines = self.__nvim.api.buf_get_lines(0, start_line - 1, stop_line, False)
        # handle edge cases of text selection
        if len(lines) == 0:
            output = ""
        elif len(lines) == 1:
            output = lines[0][start_column - 1 : stop_column]
        else:
            lines[0] = lines[0][start_column - 1 :]
            lines[-1] = lines[-1][:stop_column]
            output = "\n".join(lines)
        self.__log(LogLevel.DEBUG, f"Selected text: {output}")
        return output

    def __preprocess_input(self, text: str) -> str:
        """Preprocess the text from the buffer before evaluation.

        Args:
            text (str): Raw test from buffer

        Returns:
            str: Expression to be evaluated
        """
        # this function exists to make it easy to add more preprocessing
        # logic in the future
        return text.lstrip(" ").rstrip(" ")

    def evaluate_expression(self, expr: str) -> float | str:
        """Use asteval to evaluate the math expression.

        Args:
            expr (str): Expression to be evaluated

        Returns:
            float | str: Result of the evaluation or the provided input on error
        """
        try:
            # if the evaluation procedure succeeds, then return a float
            # of the result
            value = float(self.__aeval(expr))
        except Exception:
            # if there is any exception in the expression evaluation
            # just return the original expression so the buffer is not modified
            value = expr
        return value

    def replace_buffer_range(self, start: list[int], stop: list[int], replacement: str):
        """Replace text in a buffer.

        Args:
            start (list[int]): Start position of the text to replace
            stop (list[int]): Stop position of the text to replace
            replacement (str): String to replace the current text with
        """
        s_buf, s_row, s_col, _ = start
        _, e_row, e_col, _ = stop
        # clear the text between start and stop
        self.__nvim.api.buf_set_text(
            s_buf, s_row - 1, s_col - 1, e_row - 1, e_col, [""]
        )
        # insert the replacement text at start (will take as much space as needed)
        self.__nvim.api.buf_set_text(
            s_buf, s_row - 1, s_col - 1, s_row - 1, s_col - 1, [replacement]
        )
        # feed the escape key to exit visual mode and return to normal mode
        self.__nvim.api.feedkeys(
            self.__nvim.api.replace_termcodes("<esc>", True, False, True), "x", False
        )

    @pynvim.function("CalcNvimCalculate")
    def calculate(self, args):
        """Entrypoint to the plugin.

        Will extract the text from the currently selected range,
        evaluate it, and then replace the currently selected range with the result.
        """
        start, stop = self.get_selected_range()
        if not start or not start:
            self.__log(LogLevel.INFO, "Exiting due to error in getting selected range.")
            return

        text = self.get_text_from_range(start, stop)
        if not text:
            self.__log(
                LogLevel.INFO, "Exiting due to error in getting text at selected range."
            )

        expr = self.__preprocess_input(text)
        result = self.evaluate_expression(expr)
        self.__log(LogLevel.DEBUG, f"Result: {result}")

        if result == expr:
            self.__log(
                LogLevel.INFO,
                "Not replacing text, expression evaluation results in "
                "original expression",
            )
            return

        if isinstance(result, float):
            output = "{:{}}".format(result, self.__float_format)
        else:
            output = result

        self.replace_buffer_range(start, stop, output)
