import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s (%(asctime)s): %(message)s (Line %(lineno)d [%(filename)s])",
                    datefmt="%d/%m/%Y %H:%M:%S")
