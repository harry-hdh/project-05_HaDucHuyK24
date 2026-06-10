from config import get_mongo_client
import csv
import os
import IP2Location

#.BIN database file path
IP2LOCATION_DB_PATH = "/home/hdh99/p5_data/IP-COUNTRY-REGION-CITY.BIN"
CSV_FILE_PATH = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/ip_locations.csv"

def process_ip_loc():
    # Verify that the IP2Location database file exists
    source_col = get_mongo_client()

    if not os.path.exists(IP2LOCATION_DB_PATH):
        print(f"Error: IP2Location database not found at {IP2LOCATION_DB_PATH}")
        return
    print(f"Using IP2Location database at: {IP2LOCATION_DB_PATH}")
    # Initialize IP2Location
    ip_db = IP2Location.IP2Location(IP2LOCATION_DB_PATH)
    
    # 2. Read unique IPs from main collection using aggregation
    pipeline = [
        # Change "ip_address" to whatever your field name is
        {"$group": {"_id": "$ip"}}, 
        {"$match": {"_id": {"$ne": None}}}
    ]
    unique_ips_cursor = source_col.aggregate(pipeline)

    # Process and store results
    results = []

    for doc in unique_ips_cursor:
        ip = doc["_id"]
        
        try:
            # 3. Use ip2location to get location data
            rec = ip_db.get_all(ip)
            
            # Create a structured dictionary of the results
            if rec:
                location_data = {
                    "ip": ip,
                    "country": rec.country_long,
                    "region": rec.region,
                    "city": rec.city
                }
                results.append(location_data)
            else:
                print(f"No geolocation data found for IP: {ip}")
        except Exception as e:
            print(f"Error processing IP {ip}: {e}")
    
    if not results:
        print("No valid geolocation data found for any IPs.")
        return
    
    # 4. Write results to CSV
    # Remove existing file if it exists
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)
        print(f"Existing file in {CSV_FILE_PATH} removed.")

    keys = results[0].keys()
    with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    print(f"Successfully saved {len(results)} records to {CSV_FILE_PATH}")

#process_ip_loc()