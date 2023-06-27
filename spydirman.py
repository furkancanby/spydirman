import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sys

def download_image(url, save_directory):
    response = requests.get(url)
    if response.status_code == 200:
        image_name = os.path.join(save_directory, os.path.basename(urlparse(url).path))
        with open(image_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url}")

def scrape_images(url, save_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            absolute_url = urljoin(url, img_url)
            download_image(absolute_url, save_directory)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 spydirman.py <URL> <OUTPUT_FOLDER>")
        sys.exit(1)

    website_url = sys.argv[1]
    save_folder = sys.argv[2]

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    scrape_images(website_url, save_folder)