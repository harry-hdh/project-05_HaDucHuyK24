from config import get_mongo_client
from utils import save_to_csv


# CSV_FILE_PATH1 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info.csv"
# CSV_FILE_PATH2 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_referrer_url.csv"


def extract_product_data(collection, target_events, fields_to_extract, output_csv_path, id_fallbacks=None):

    # 1. Base Match Stage (Filters event types)
    pipeline = [
        {"$match": {"collection": {"$in": target_events}}}
    ]
    # 2. Dynamically build the $project stage
    project_stage = {
        "_id": 0,
        "event_type": "$collection"  # Always keep track of which event it came from
    }

    for field in fields_to_extract:
        project_stage[field] = 1

    if id_fallbacks:
        for target_field, fallback_list in id_fallbacks.items():
            project_stage[target_field] = {"$ifNull": fallback_list}

    pipeline.append({"$project": project_stage})

    # 3. Filter out records where the main identifier ended up null
    if id_fallbacks:
        # Grabs the first target field defined (usually product_id) to ensure it's not empty
        main_id = list(id_fallbacks.keys())[0]
        pipeline.append({"$match": {main_id: {"$ne": None}}})

    #Running aggregation query on MongoDB
    cursor = collection.aggregate(pipeline)
    # Convert cursor to a list of dicts to write to CSV
    extracted_records = list(cursor)

    # Save data to csv 
    if extracted_records:
        fieldnames = list(extracted_records[0].keys())  
        save_to_csv(extracted_records, fieldnames, output_csv_path)
    else:
        print("No matching event data found based on your criteria.")


# collections = [
#     "view_product_detail",
#     "select_product_option",
#     "select_product_option_quality",
#     "add_to_cart_action",
#     "product_detail_recommendation_visible",
#     "product_detail_recommendation_noticed"
# ]
# product_id_fallback = {"product_id": ["$product_id", "$viewing_product_id"]}

#extract_product_data(collection=get_mongo_client(), target_events=collections, fields_to_extract=["current_url"], id_fallbacks=product_id_fallback, output_csv_path=CSV_FILE_PATH1)

#extract_product_data(collection=get_mongo_client(), target_events=[ "product_view_all_recommend_clicked" ], fields_to_extract=["referrer_url"], id_fallbacks={"product_id": ["$viewing_product_id", "$product_id"]}, output_csv_path=CSV_FILE_PATH2)