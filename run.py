from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build 
from googleapiclient.http import BatchHttpRequest
import httplib2
import json
from colorama import Fore, Style, init
import os
from xml.dom import minidom
import requests

init()

JSON_KEY_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

if not os.path.isfile(JSON_KEY_FILE):
    print(f"{Fore.RED}{Style.BRIGHT}File credentials.json tidak ditemukan. Pastikan file tersebut ada dan bernama dengan benar.{Style.RESET_ALL}")
    exit()

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
except Exception as e:
    print(f"{Fore.RED}{Style.BRIGHT}Terjadi kesalahan dalam memuat credentials.json. Pastikan file tersebut berisi kredensial yang benar.{Style.RESET_ALL}")
    exit()

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

def get_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        xml_content = response.content
        dom = minidom.parseString(xml_content)
        urls = [url.firstChild.nodeValue for url in dom.getElementsByTagName('loc')]
        return urls
    except Exception as e:
        print_error(f"Terjadi kesalahan saat mengambil URL dari sitemap: {e}")
        return []

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
    print("3. Mass Submit URL")
    print("0. Keluar")
    choice = input("Pilih alat (0-3): ")
    url = ""
    if choice == "1":
        url = input("Masukkan URL yang ingin diindeks: ")
        send_url(url)
    elif choice == "2":
        url = input("Masukkan URL yang ingin dihapus: ")
        delete_url(url)
    elif choice == "3":
        sitemap_url = input("Masukkan URL sitemap: ")
        urls = get_urls_from_sitemap(sitemap_url)
        if urls:
            for url in urls:
                send_url(url)
        else:
            print_error("Tidak dapat mengambil URL dari sitemap.")
    elif choice == "0":
        return False
    else:
        print_error("Pilihan tidak valid.")
    return True

if __name__ == "__main__":
    while get_user_input():
        pass


