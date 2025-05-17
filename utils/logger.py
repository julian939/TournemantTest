import logging

def setup_logger():
    logging.getLogger("discord").setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("./data/bot.log"),     
            logging.StreamHandler()              
        ]
    )
