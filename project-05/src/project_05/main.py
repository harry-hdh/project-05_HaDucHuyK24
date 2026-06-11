from collect_product_info import extract_product_data
from scrape_product_name import scrape_main
from process_ip_loc import process_ip_loc

#
IP2LOCATION_DB_PATH = "/home/hdh99/p5_data/IP-COUNTRY-REGION-CITY.BIN"
IP_CSV_FILE_PATH = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/ip_locations.csv"
PRODUCT_CSV_FILE_PATH1 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_referrer_url.csv"
PRODUCT_CSV_FILE_PATH2 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info.csv"
SAVE_PATH1 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_with_titles1.csv"
SAVE_PATH2 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_with_titles2.csv"

if __name__ == "__main__":
    # Process IP locations 
    process_ip_loc(IP2LOCATION_DB_PATH, IP_CSV_FILE_PATH)

    # Extract product info and referrer URLs from MongoDB and save to CSV
    collections = [
    "view_product_detail",
    "select_product_option",
    "select_product_option_quality",
    "add_to_cart_action",
    "product_detail_recommendation_visible",
    "product_detail_recommendation_noticed"
    ]

    product_id_fallback = {"product_id": ["$product_id", "$viewing_product_id"]}

    extract_product_data(collection=get_mongo_client(), target_events=collections, fields_to_extract=["current_url"], id_fallbacks=product_id_fallback, output_csv_path=PRODUCT_CSV_FILE_PATH1)

    extract_product_data(collection=get_mongo_client(), target_events=[ "product_view_all_recommend_clicked" ], fields_to_extract=["referrer_url"], id_fallbacks={"product_id": ["$viewing_product_id", "$product_id"]}, output_csv_path=PRODUCT_CSV_FILE_PATH2)

    # Scrape product titles for URLs in CSV and save to new CSV
    URLS1 = [record["referrer_url"] for record in read_product_csv(PRODUCT_CSV_FILE_PATH1)]
    URLS2 = [record["referrer_url"] for record in read_product_csv(PRODUCT_CSV_FILE_PATH2)]

    asyncio.run(scrape_main(SAVE_PATH1, URLS1))
    asyncio.run(scrape_main(SAVE_PATH2, URLS2))