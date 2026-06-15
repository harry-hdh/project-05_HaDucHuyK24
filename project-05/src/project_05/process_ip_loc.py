from con import get_mongo_client
from utils import save_to_csv
import os
import IP2Location



def process_ip_loc(bin_path, output_csv_path):
    # Verify that the IP2Location database file exists
    source_col = get_mongo_client()

    if not os.path.exists(bin_path):
        print(f"Error: IP2Location database not found at {bin_path}")
        return
    print(f"Using IP2Location database at: {bin_path}")
    # Initialize IP2Location
    ip_db = IP2Location.IP2Location(bin_path)
    
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

    keys = results[0].keys()
    
    save_to_csv(results, keys, output_csv_path)

#process_ip_loc()