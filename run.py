from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build 
from googleapiclient.http import BatchHttpRequest
import httplib2
import json
from colorama import Fore, Style, init

init()

JSON_KEY_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())

def delete_url(url):
    content = {
        'url': url,
        'type': "URL_DELETED"
    }
    json_content = json.dumps(content)
    response, content = http.request(ENDPOINT, method="POST", body=json_content)
    result = json.loads(content.decode())

    if 'urlNotificationMetadata' in result:
        print_success(f"URL deleted: {result['urlNotificationMetadata']['url']}")
        print_success(f"Notify Time: {result['urlNotificationMetadata']['latestUpdate']['notifyTime']}\n")
    else:
        print_error(f"Error in response: {result}")

def send_url(url):
    content = {
        'url': url,
        'type': "URL_UPDATED"
    }
    json_content = json.dumps(content)
    response, content = http.request(ENDPOINT, method="POST", body=json_content)
    result = json.loads(content.decode())


    if 'urlNotificationMetadata' in result:
        print_success(f"URL: {result['urlNotificationMetadata']['url']}")
        print_success(f"Type: {result['urlNotificationMetadata']['latestUpdate']['type']}")
        print_success(f"Notify Time: {result['urlNotificationMetadata']['latestUpdate']['notifyTime']}\n")
    else:
        print_error(f"Error in response: {result}")

def print_success(message):
    print(f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}")

def get_user_input():
    banner = '''
    ⠀⠀⠀⠀⠀⠀  ⠀⢀⠀⠀⠀⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⡄⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⡸⢐⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢿⡙⠶⢄⣀⠀⢫⠒⢤⣀⠀⠀⢸⠰⠀⠀⣀⡤⣤⠤⠀⠀⠀
⠀⠀⠀⠀⠉⢒⠦⠄⠈⠉⠁⠠⠀⠉⠉⠙⠃⠚⠉⣠⠎⠀⠀⠀⠀⠀
⢀⣄⣠⡐⣈⡀⡄⠀⠀⢠⠀⢀⣴⣠⠀⠀⠀⠀⠀⠻⣀⠀⠀⠀⠀⠀▒█▀▀█ ░░ ▀█▀ ▒█▄░▒█ ▒█▀▀▄ ▒█▀▀▀ ▀▄▒▄▀ 
⠀⠀⢨⠟⢁⢔⡁⢀⠔⠀⠐⣡⣯⠃⢠⠀⡆⢤⠀⡀⢰⡯⡒⠠⠤⠀▒█░▄▄ ▀▀ ▒█░ ▒█▒█▒█ ▒█░▒█ ▒█▀▀▀ ░▒█░░ 
⢀⣴⡵⣾⢗⣥⣶⣿⣷⣮⡼⢣⠃⢠⣧⣤⣯⣘⠀⢣⠀⣣⡏⠉⠚⠉▒█▄▄█ ░░ ▄█▄ ▒█░░▀█ ▒█▄▄▀ ▒█▄▄▄ ▄▀▒▀▄⠀⠀⠀
⠟⠁⣸⣣⡃⢿⣿⣿⣿⣿⠷⠾⢶⣿⣿⣿⣿⣿⡆⣿⡀⢿⣸⡀⠀⠀[ Google Indexing Using Indexing Api ]
⠀⢰⠋⠀⠀⠀⠉⠙⠉⠁⢀⣀⡀⠙⠛⠛⠛⠛⠑⡿⣯⣽⠋⣳⡆⠀
⠀⠈⠳⢦⣄⡀⠀⠀⠘⣄⣀⣀⠼⠃⠀⠀⢀⠀⠠⠴⠿⠛⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠉⠉⠓⠒⠒⠤⠤⠤⠤⠔⠚⠁⠀⠀⠀⠀⠀'''
    print(banner)
    print("Github: DomathID")
    print("=== Menu Alat ===")
    print("1. Kirim URL")
    print("2. Hapus URL")
    print("0. Keluar")
    choice = input("Pilih alat (0-2): ")
    url = ""
    if choice == "1":
        url = input("Masukkan URL yang ingin diindeks: ")
        send_url(url)
    elif choice == "2":
        url = input("Masukkan URL yang ingin dihapus: ")
        delete_url(url)
    elif choice == "0":
        return False
    else:
        print_error("Pilihan tidak valid.")
    return True


if __name__ == "__main__":
    while get_user_input():
        pass

