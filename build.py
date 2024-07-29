import platform
import os
import sys
import time
import zipfile

import py7zr
import requests

BUILD_DIR = "./build"
DOWNLOAD_DIR = f"{BUILD_DIR}/downloads"


def download(url, filename):
    print("Downloading from", url)
    # Download code here
    # Create directory if not exists
    if not os.path.exists(f"{DOWNLOAD_DIR}"):
        os.makedirs(f"{DOWNLOAD_DIR}")
    
    if os.path.exists(f"{DOWNLOAD_DIR}/{filename}"):
        print(f"{filename} already exists.")
        return
    
    print(f"Downloading {filename} ...")

    start = time.time()
    response = requests.get(url, stream=True)
    size = 0
    chunk_size = 1024
    total_size = int(response.headers.get("content-length", 0))
    with open(f"{DOWNLOAD_DIR}/{filename}", "wb") as file:
        for data in response.iter_content(chunk_size=chunk_size):
            size += len(data)
            file.write(data)
            print(f"\rDownloading... {size}/{total_size} [{size * 100 / total_size:.2f}%]", end="")
    print()

def build():
    print("Building...")

    # Download Sarasa Gothic
    download("https://github.com/be5invis/Sarasa-Gothic/releases/download/v1.0.16/Sarasa-TTF-1.0.16.7z", "Sarasa.7z")
    
    # Extract Sarasa Gothic
    print("Extracting Sarasa.7z ...")
    archive = py7zr.SevenZipFile(f"{DOWNLOAD_DIR}/Sarasa.7z", mode="r")
    archive.extractall(f"{BUILD_DIR}/Sarasa")
    archive.close()
    print("Extract done.")

    # Remove non SC files
    for file in os.listdir(f"{BUILD_DIR}/Sarasa"):
        if file.find("SC") == -1:
            os.remove(f"{BUILD_DIR}/Sarasa/{file}")
    
    # Download FontPatcher
    download("https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FontPatcher.zip", "FontPatcher.zip")
    # Extract FontPatcher
    print("Extracting FontPatcher.zip ...")
    with zipfile.ZipFile(f"{DOWNLOAD_DIR}/FontPatcher.zip", "r") as zip_ref:
        zip_ref.extractall(f"{BUILD_DIR}/FontPatcher")

    # Patch Sarasa Gothic
    print("Patching Sarasa Gothic ...")
    for ttf in os.listdir(f"{BUILD_DIR}/Sarasa"):
        print(f"Patching {ttf} ...")
        os.system(f"python3 {BUILD_DIR}/FontPatcher/font-patcher --complete --outputdir {BUILD_DIR}/SarasaNerds {BUILD_DIR}/Sarasa/{ttf}")
        print(f"Patched {ttf} done.")
    print("Patch done.")

    print("Build done.")


def main(args):
    if platform.uname().version.find("Ubuntu") == -1:
        print("Sorry, this script is only for Ubuntu.")
        return 1
    
    if args.__len__() < 2:
        print("Usage: python3 build.py [clean|deps|build]")
        return 1
    
    if args[1] == "clean":
        print("Cleaning...")
        os.system(f"rm -rf {BUILD_DIR}")
        print("Clean done.")
        return 0
    if args[1] == "deps":
        print("Installing dependencies...")
        os.system("sudo apt install python3-py7zr python3-fontforge")
        return 0
    if args[1] == "build":
        build()
        return 0


if __name__ == "__main__":
    main(sys.argv)