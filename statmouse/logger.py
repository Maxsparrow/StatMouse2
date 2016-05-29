import logging.config
import logging.handlers


def set_logging(project_name, logging_path='mylog.log'):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(project_name)
    logger.setLevel(logging.DEBUG)

    filehandler = logging.handlers.TimedRotatingFileHandler(filename=logging_path, when='D', backupCount=7)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.DEBUG)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    logger.info("Logger started")
