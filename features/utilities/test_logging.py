import logging
from features.steps.config import Environment

log_level = Environment.LOG_LEVEL1


def test_log():
    # if os.path.exists('logger.log'):
    # os.remove('logger.log')
    logger = logging.getLogger(__name__)
    fileHandler = logging.FileHandler('logger.log')
    logFormat = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    fileHandler.setFormatter(logFormat)
    logger.addHandler(fileHandler)  # in which file we need to add this
    logger.setLevel(logging.getLevelName(log_level))
    # stream handler for console logging
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormat)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.getLevelName(log_level))
    return logger
