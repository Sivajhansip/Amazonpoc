import logging
import os


def test_log():
    if os.path.exists('logger.log'):
        os.remove('logger.log')
    logger = logging.getLogger(__name__)
    fileHandler = logging.FileHandler('logger.log')
    logFormat = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    fileHandler.setFormatter(logFormat)
    logger.addHandler(fileHandler)  # in which file we need to add this
    logger.setLevel(logging.DEBUG)
    # stream handler for console logging
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormat)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)
    return logger
