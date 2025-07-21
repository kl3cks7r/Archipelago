import requests
import os

# from worlds.cave_story import CaveStoryWorld
# DOWNLOAD_DIR = CaveStoryWorld.settings.game_dir
DOWNLOAD_DIR = "C:/ProgramData/Archipelago/CaveStoryInstances"
API_URL = f"https://api.github.com/repos/cave-story-randomizer/cave-story-randomizer/releases/latest"


def fetch_latest_release_info():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def download_assets(release_info, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    download_url = release_info['zipball_url']
    print(f"Downloading {download_url}...")
    asset_data = requests.get(download_url)
    asset_data.raise_for_status()
    with open(os.path.join(download_dir, release_info["tag_name"] + ".zip"), "wb") as f:
        f.write(asset_data.content)
    print(f"Saved to {os.path.join(download_dir, release_info['tag_name'] + '.zip')}")

def main():
    release_info = fetch_latest_release_info()
    tag_name = release_info["tag_name"]
    print(f"Latest Release Info: {tag_name}")

    if not os.path.exists(os.path.join(DOWNLOAD_DIR, tag_name + '.zip')):
        download_assets(release_info, DOWNLOAD_DIR)
    else:
        print(f"Release {tag_name} already downloaded.")

if __name__ == "__main__":
    main()
