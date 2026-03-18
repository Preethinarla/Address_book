import logging , os
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# logger = logging.getLogger("Book") 


def log_handle():
    logger = logging.getLogger("Book")
    logger.setLevel(logging.ERROR) 
    file_handler = logging.FileHandler('Book.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s- %(module)s - %(lineno)d - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler) 
    if os.path.getsize("Book.log")>2000:
        os.truncate("Book.log",2) 
        
    return logger
