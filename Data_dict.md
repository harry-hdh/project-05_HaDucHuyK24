| Field | Type | Description |
| ----- | ---- | ----------- |
| _id | ObjectId | Unique identifier of the user's session |
| time_stamp | Int32 | unix time stamp when session was logged |
| ip | String | IP address of user |
| user_id_db | String | User id in DB (if registered) |
| user_agent | String | Web browser agent info |
| resolution | String | Resolution of device (phone/table/pc) |
| device_id | String | Id of device |
| api_version | String | Version of api |
| store_id | String | ID of store based on country |
| show_recommendation | String | True or false if recommendatation is showed |
| current_url | String | current url of user |
| referrer_url | String | previous url of current url |
| email_address | String | User's address |
| collection | String | Action of user |
| product_id | String | Product id |
| price | String | Price of item (collection = add_to_cart_action) |
| currency | String | currency of price (collection = add_to_cart_action) |
| is_paypal | null | (collection = add_to_cart_action) |
| option | Array |  |
| alloy | String | material cat (collection = view_listing_page) |
| diamond | String | material cat (collection = view_listing_page) |
| shapediamond | String | material cat (collection = view_listing_page) |
| option_label | String | (collection = view_product_detail) |
| option_id | String | (collection = view_product_detail) |
| value_label | String | (collection = view_product_detail) |
| value_id | String | (collection = view_product_detail) |
| quality | String | Diamond type |
| quality_label | boolean | Label |
| cat_id | boolean | (if collection = view_listing_page) |
| quality_label | boolean | (if collection = view_listing_page) |
| key_search | boolean | (collection = search_box_action) |
