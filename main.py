# main.py

import os
from other.updater import check_for_updates
from other.VERSION import VERSION

def main():
    check_for_updates()
    os.system(f"title GAME WIP version: {VERSION} ")
    print(f"Placeholder (Version {VERSION})")


if __name__ == "__main__":
    main()
