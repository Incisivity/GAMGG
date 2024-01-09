import requests
import zipfile
import os
import sys
import shutil
from other.VERSION import VERSION

def get_latest_release_version(repo_owner, repo_name):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    response = requests.get(api_url)
    data = response.json()

    # Print the API response for debugging
    print("GitHub API Response:", data)

    # Update this line based on the actual structure of the response
    return data['tag_name']

def is_update_available(current_version, latest_version):
    return current_version < latest_version

def download_and_extract_update(repo_owner, repo_name, latest_version):
    url = f'https://github.com/{repo_owner}/{repo_name}/archive/{latest_version}.zip'
    zip_file_path = 'update.zip'
    response = requests.get(url)
    
    with open(zip_file_path, 'wb') as zip_file:
        zip_file.write(response.content)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Extract to a temporary directory
        extract_path = 'update_temp'
        zip_ref.extractall(extract_path)

    # Clean up the downloaded ZIP file
    os.remove(zip_file_path)

    return extract_path

def replace_current_code(update_path):
    # Replace the current code with the updated code
    current_path = os.path.dirname(os.path.abspath(__file__))
    
    for file_name in os.listdir(update_path):
        file_path = os.path.join(update_path, file_name)
        destination_path = os.path.join(current_path, file_name)
        if os.path.isdir(file_path):
            shutil.rmtree(destination_path, ignore_errors=True)
            shutil.move(file_path, destination_path)
        else:
            shutil.copy2(file_path, destination_path)

    # Clean up the temporary update directory
    shutil.rmtree(update_path, ignore_errors=True)

def check_for_updates():
    repo_owner = "YourGitHubUsername"
    repo_name = "YourGameRepository"

    current_version = VERSION
    latest_version = get_latest_release_version(repo_owner, repo_name)

    if is_update_available(current_version, latest_version):
        print(f"Update available: {current_version} -> {latest_version}")
        update_path = download_and_extract_update(repo_owner, repo_name, latest_version)
        replace_current_code(update_path)
        print("Update complete. Please restart the game.")
        sys.exit()
    else:
        print("No update available.")

if __name__ == "__main__":
    check_for_updates()
