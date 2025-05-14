import sys

import supernote
from dotenv import dotenv_values
from datetime import datetime
import subprocess

config = dotenv_values('.env')

sn_username = config['SUPERNOTE_USERNAME']
sn_password = config['SUPERNOTE_PASSWORD']
ft_username = config['FT_USERNAME']
ft_password = config['FT_PASSWORD']

news_folder = 1124245997816381441
file_prefix = "Financial Times_"
date = datetime.now().strftime("%Y-%m-%d")
file_name = f"{file_prefix}{date}.pdf"


def list_news(t):
    files = supernote.file_list(t, news_folder)
    return files

def download_news():
    result = subprocess.run(['ebook-convert', 'ft.recipe', file_name, '--username='+ft_username, '--password='+ft_password], capture_output=True)


def upload_news():
    supernote.upload_file(token, file_name, directory=news_folder)

def get_token_from_file():
    try:
        with open('token.txt', 'r') as token_file:
            token = token_file.read()
    except FileNotFoundError:
        token = None
    return token

def check_token():
    token = get_token_from_file()
    try:
        supernote.file_list(token)
        return token
    except Exception:
        print("Token expired, logging in again")
        token = supernote.login(sn_username, sn_password)
        print(token)
        with open('token.txt', 'w') as token_file:
            token_file.write(token)
        try:
            supernote.file_list(token)
            return token
        except Exception:
            return None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    token = check_token()
    if token is None:
        print("Couldn't log in to supernote cloud, exiting...")
        sys.exit(1)

    upload_news()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
