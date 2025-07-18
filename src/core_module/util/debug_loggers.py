import logging
import inspect

# ANSI escape codes
LIGHT_GRAY = "\033[90m"
LIGHT_BLUE = "\033[94m"
RESET = "\033[0m"


class TreeStackFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            # Show call stack tree for DEBUG level
            stack = inspect.stack()
            frames = stack[6:11]
            tree_lines = []

            for i, frame in enumerate(reversed(frames)):
                filename = frame.filename.rsplit("/", 1)[-1]
                lineno = frame.lineno
                func = frame.function
                indent = "|   " * i
                tree_lines.append(f"{indent}|--- [{LIGHT_GRAY}{filename}:{lineno}{RESET}] {func}()")

            tree = "\n".join(tree_lines)
            base = super().format(record)
            return f"{tree}\n[{LIGHT_BLUE}{record.filename}:{record.lineno}{RESET}] {base}"

        # For INFO and above: just one line
        return f"[{LIGHT_BLUE}{record.filename}:{record.lineno}{RESET}] {record.getMessage()}"


def setup_logger():
    """
    Call once in your main entrypoint.
    Use logger = logging.getLogger("src")
    """
    formatter = TreeStackFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.WARNING)

    src_logger = logging.getLogger("src")
    src_logger.setLevel(logging.DEBUG)
    src_logger.addHandler(handler)
    src_logger.propagate = False
