import logging


class CustomLogger(object):
    logger = None

    @staticmethod
    def prepare_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('ImgApp.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
                    "%(asctime)s - %(levelname)s [%(module)s] (%(process)d:%(thread)d) --> %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    @staticmethod
    def get_instance():
        if not CustomLogger.logger:
            CustomLogger.logger = CustomLogger.prepare_logger()
        return CustomLogger.logger
