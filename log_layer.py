# log_layer.py

import json
import logging
import sys

try:
    from rich.console import Console
    from rich.theme import Theme

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)


class RichFormatter(logging.Formatter):
    def __init__(self):
        custom_theme = Theme(
            {
                "info": "green",
                "warning": "yellow",
                "error": "bold red",
                "debug": "dim cyan",
            }
        )
        self.console = Console(theme=custom_theme)
        super().__init__()

    def format(self, record):
        level = record.levelname.lower()
        style = {
            "info": "info",
            "warning": "warning",
            "error": "error",
            "debug": "debug",
        }.get(level, "none")
        formatted = (
            f"[{style}]{record.levelname:<8} {record.name:<20}[/] {record.getMessage()}"
        )
        return formatted


class DevConsoleHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)
        self.formatter = (
            RichFormatter()
            if RICH_AVAILABLE
            else logging.Formatter("%(levelname)s - %(name)s - %(message)s")
        )

    def emit(self, record):
        try:
            msg = self.format(record)
            print(msg)
        except Exception:
            self.handleError(record)


class JsonFileHandler(logging.FileHandler):
    def __init__(self, filename="system_log.json"):
        super().__init__(filename)
        self.setFormatter(JsonFormatter())


def setup_logging(env="dev"):
    logging.root.handlers = []  # clear existing handlers

    if env == "dev":
        handler = DevConsoleHandler()
    else:
        handler = JsonFileHandler()

    handler.setLevel(logging.DEBUG)
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)


def get_logger(name):
    return logging.getLogger(name)
