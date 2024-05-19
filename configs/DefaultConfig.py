import configparser

config = configparser.ConfigParser()
config.read('config.ini')

DISCORD_OWNER_ID = config['DEFAULT']['discord_owner_id']
DISCORD_SDK_TOKEN = config['DEFAULT']['discord_sdk_token']
GEMINI_API = config['DEFAULT']['gemini_api_authen']
