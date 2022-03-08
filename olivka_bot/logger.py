import logging


def get_logger(name: str, log_path: str, level: str) -> logging.Logger:
    """
    Setting up the logging tool
     :param name: module name
    :param log_path: path to the file to save the log
    :param level: logging level
    :return: logger
    """

    logger = logging.getLogger(name)
    log_format = "[%(asctime)s %(name)s %(levelname)s] %(message)s"

    if level is not None:
        logger.setLevel(level)

    if log_path:
        fh = logging.FileHandler(filename=log_path)
        fh.setFormatter(logging.Formatter(log_format))
        logger.addHandler(fh)
    else:
        logging.basicConfig(
            format=log_format,
        )
    return logger
