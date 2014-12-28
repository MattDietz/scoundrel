import logging

# TODO(mdietz): make this configurable
FORMAT = "[%(levelname)s - %(asctime)s %(pathname)s:"\
         "%(lineno)d] %(message)s"
LOG = logging

class ScoundrelLogger(logging.Logger):
    def __init__(self, name, level=None):
        formatter = logging.Formatter(FORMAT)

        # TODO(mdietz): make this configurable
        logging.Logger.__init__(self, name,
                                logging.getLevelName("DEBUG"))
        handlers = []
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)
        # TODO(mdietz): make this configurable
        logfile = "scoundrel.log"
        if logfile:
            file_handler = logging.FileHandler(filename=logfile)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        for handler in handlers:
            logging.Logger.addHandler(self, handler)


def setup_logging():
    logging.root = ScoundrelLogger("ScoundrelLogger")
    logging.setLoggerClass(ScoundrelLogger)
