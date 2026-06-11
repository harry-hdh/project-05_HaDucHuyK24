import csv
import os

def save_to_csv(data, headers, file_path):
    # Remove existing file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Existing file in {file_path} removed.")

    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=headers)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} records to {file_path}")

# read csv file and remove duplicates based on product_id, remevoe missing referrer_url, and return a list of referrer_url
def read_product_csv(file_path):
    unique_records = {}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_id = row.get('product_id')
            referrer_url = row.get('referrer_url')
            if product_id and referrer_url:  # Ensure both fields are present
                unique_records[product_id] = referrer_url  # This will automatically handle duplicates by overwriting
    #return [url for pid,url in unique_records.items()]            
    return [{"product_id": pid, "referrer_url": url} for pid, url in unique_records.items()]
    

# print(read_product_csv("/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_referrer_url.csv"))