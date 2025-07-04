import os
import json
import re
from datetime import datetime
from glob import glob

def parse_filename(filename):
    print(filename)
    # C:\Users\Mark\Downloads\python3-ptxprint_2.3.32-0~202308011027~ubuntu22.04.1_all.deb  # old
                            # python3-ptxprint_2.8.17-0~20250624~ubuntu24.10.1_all.deb      # new
    pattern = r'(?P<path>.+)\\(?P<name>.+)_(?P<version>\d+(\.\d+)+)-\d+~(?P<date>\d{8})~(?P<platform>.+)(?P<edition>\d\d\.\d\d)\.\d_.+?\.(?P<extension>.+)'
    match = re.match(pattern, filename)
    if match:
        groups = match.groupdict()
        groups['date'] = datetime.strptime(groups['date'], '%Y%m%d').strftime('%Y-%m-%d')
        return groups
    else:
        raise ValueError("Invalid filename format")

def create_download_info(filename):
    file_info = parse_filename(filename)
    download_info = {
        "name": "PTXPrint Linux " + file_info['edition'],
        "version": file_info['version'],
        "date": file_info['date'],
        "edition": "",
        "platform": "linux",
        "platform_version": "Ubuntu " + file_info['edition'] + " LTS",
        "architecture": "amd64",
        "stability": "stable",
        "nature": "ver2",
        "file": os.path.basename(filename),
        "md5": "",
        "type": file_info['extension'],
        "build": ""
    }
    download_info_filename = os.path.join(file_info['path'], filename[:-4] + ".download_info")
    with open(download_info_filename, 'w') as file:
        json.dump(download_info, file, indent=2)

def process_recent_files():
    # "C:\Users\mark-\Downloads\python3-ptxprint_2.4.5-0~202311291235~ubuntu22.04.1_all.deb"
    download_folder = r'C:\Users\mark-\Downloads'
    file_pattern = 'python3-ptxprint_*.deb'
    deb_files = glob(os.path.join(download_folder, file_pattern))
    deb_files.sort(key=os.path.getmtime, reverse=True)

    for deb_file in deb_files[:3]:  # Process the three most recent files
        try:
            create_download_info(deb_file)
            print(f"Download info file created: {os.path.basename(deb_file)}.download_info")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        process_recent_files()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        try:
            create_download_info(filename)
            print(f"Download info file created: {os.path.basename(filename)}.download_info")
        except ValueError as e:
            print(e)
    else:
        print("Usage: python buildDownloadInfo4deb.py [filename]")
