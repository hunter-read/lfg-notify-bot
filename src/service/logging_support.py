import logging
import os


def init_logger() -> logging.Logger:
    logger = logging.getLogger("lfg-notify-bot")
    log_file = os.environ.get('LOG_FILE')
    log_level = os.environ.get('LOG_LEVEL', logging.ERROR)

    hdlr = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    str_format = "%(levelname)s:%(asctime)s: %(message)s"
    hdlr.setFormatter(logging.Formatter(str_format, "%Y-%m-%d %H:%M:%S"))

    logger.addHandler(hdlr)
    logger.setLevel(log_level)
    return logger
