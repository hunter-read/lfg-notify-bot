import logging
import praw


def init_logger(bot_name: str, reddit: praw.Reddit) -> logging.Logger:
    logger = logging.getLogger(bot_name)
    log_file = reddit.config.custom["log_file"]
    log_level = reddit.config.custom[f"log_level_{bot_name}"]

    hdlr = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    str_format = "%(levelname)s:%(name)s:%(asctime)s: %(message)s" if log_file else "%(levelname)s: %(message)s"
    hdlr.setFormatter(logging.Formatter(str_format, "%Y-%m-%d %H:%M:%S"))

    logger.addHandler(hdlr)
    logger.setLevel(log_level if log_level else logging.ERROR)
    return logger
