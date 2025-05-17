import json
import os
from dotenv import load_dotenv
import logging

def load_json(json_path):
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error("Couldnt load json file.")

def save_json(config, json_path):
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error("Couldnt save json file.")

def load_config():
    return load_json("./configs/config.json")

def save_config(config):
    save_json(config, "./configs/config.json")

def load_stream_config():
    return load_json("./configs/stream_config.json")

def save_stream_config(config):
    save_json(config, "./configs/stream_config.json")

def load_env():
    load_dotenv()
    config = {}

    config["DISCORD_TOKEN"] = os.getenv("DISCORD_TOKEN")
    config["DISCORD_SERVER_ID"] = os.getenv("DISCORD_SERVER_ID")
    config["TWITCH_CLIENT_ID"] = os.getenv("TWITCH_CLIENT_ID")
    config["TWITCH_CLIENT_SECRET"] = os.getenv("TWITCH_CLIENT_SECRET")
    config["DATABASE_LOCATION"] = os.getenv("DATABASE_LOCATION")

    return config