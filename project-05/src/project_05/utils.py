import csv
import os
import re
import json
from pathlib import Path

def chunked(lst, size):
    for i in range(0,len(lst), size):
        yield lst[i:i + size]

# Remove file if it exists
def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Existing file in {file_path} removed.")

# Get list of files in a folder
def list_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        return files
    except Exception as e:
        print(f"Error listing files in {folder_path}: {e}")
        return []

def save_batch_csv(data, headers, file_name, batch_num, folder_name):
    file_path = f"{folder_name}/{file_name}_{batch_num}.csv"
    if os.path.exists(file_path):
        os.remove(file_path)

    Path(folder_name).mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=headers)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} records to {file_path}")


def save_to_csv(data, headers, file_path, mode='w'):
    if mode == 'w':
        if os.path.exists(file_path): # Remove existing file if it exists
            os.remove(file_path)
            print(f"Existing file in {file_path} removed.")

        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=headers)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"Successfully saved {len(data)} records to {file_path}")
    elif mode == 'a':
        with open(file_path, 'a', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=headers)
            dict_writer.writerows(data)
        print(f"Successfully appended {len(data)} records to {file_path}")
    else:
        print(f"Invalid mode '{mode}' specified. Use 'w' for write or 'a' for append.")

# read csv file and remove duplicates based on product_id, remevoe missing referrer_url, and return a list of referrer_url
def read_product_csv(file_path, url_field, id_field="product_id"):
    unique_records = {}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_id = row.get(id_field)
            url = row.get(url_field)
            if product_id and url:  # Ensure both fields are present
                unique_records[product_id] = url  # This will automatically handle duplicates by overwriting
    #return [url for pid,url in unique_records.items()]            
    return [{"product_id": pid, url_field: url} for pid, url in unique_records.items()]
    

# print(read_product_csv("/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_referrer_url.csv"))

# Process json data
def process_json_data(soup, url):
    script_tag = soup.find('script', string=re.compile(r'react_data'))
    if script_tag:
        try:
            json_data = re.search(r'var\s+react_data\s*=\s*(.*?"gender"\s*:\s*[^,}]+)(?=[,}])', script_tag.string).group(1) + "}"
            
            data = json.loads(json_data)

            product_id = data.get('product_id', 'No Product ID Found')
            title = data.get('name', 'No Title Found')
            product_info = data

            return {
                "title": title,
                "url": url,
                "product_info": product_info
            }
        except Exception as e:
            print(f"Error parsing JSON for {url}: {e}")
            return {"title": "Failed to Parse JSON", "url": url, "product_info": {}}
    else:
        print(f"No react_data script tag found for {url}")
        return {"title": "No react_data Found", "url": url, "product_info": {}}