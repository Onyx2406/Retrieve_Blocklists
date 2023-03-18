import os
import sys
import datetime
import configparser
import requests

def download_blocklist(url, destination_folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(destination_folder, f"{datetime.date.today().strftime('%Y-%m-%d')}_{url.split('/')[-1]}")
        with open(filename, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded blocklist from {url} and saved as {filename}")
    else:
        print(f"Failed to download blocklist from {url}: status code {response.status_code}")

def main(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    destination_folder = config.get('settings', 'destination_folder')
    os.makedirs(destination_folder, exist_ok=True)

    sources = config.items('sources')
    for _, source_url in sources:
        download_blocklist(source_url, destination_folder)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python blocklist_downloader.py <config_file>")
        sys.exit(1)
    config_file = sys.argv[1]
    main(config_file)
