CUSTOMERS_PRIMARY_KEY = ["customer_id"]

CUSTOMERS_COLUMNS = {
    "customer_id": "str",
    "customer_unique_id": "str",
    "customer_zip_code_prefix": "str",
    "customer_city": "str",
    "customer_state": "str"
}

ORDERS_PRIMARY_KEY = ["order_id"]

ORDERS_COLUMNS = {
    'order_id': "str", 
    'customer_id': "str", 
    'order_status': "str", 
    'order_purchase_timestamp': "datetime",
    'order_approved_at': "datetime", 
    'order_delivered_carrier_date': "datetime",
    'order_delivered_customer_date': "datetime", 
    'order_estimated_delivery_date': "datetime"
}

ORDER_ITEMS_PRIMARY_KEY = ['order_id', 'order_item_id']

ORDER_ITEMS_COLUMNS = {
    'order_id': "str", 
    'order_item_id': "int", 
    'product_id': "str", 
    'seller_id': "str",
    'shipping_limit_date': "datetime", 
    'price': "float", 
    'freight_value': "float"
}


ORDER_PRODUCTS_PRIMARY_KEY = ["product_id"]

ORDER_PRODUCTS_COLUMNS = {
    'product_id': "str", 
    'product_category_name': "str", 
    'product_name_lenght': "int",
    'product_description_lenght': "int", 
    'product_photos_qty': "int", 
    'product_weight_g': "float",
    'product_length_cm': "float", 
    'product_height_cm': "float", 
    'product_width_cm': "float"
}

ORDER_PAYMENTS_PRIMARY_KEY = ["order_id", "payment_sequential"]

ORDER_PAYMENTS_COLUMNS = {
    'order_id': "str", 
    'payment_sequential': "int", 
    'payment_type': "str",
    'payment_installments': "int", 
    'payment_value': "float"
}


SELLERS_PRIMARY_KEY = ["seller_id"]

SELLERS_COLUMNS = {
    'seller_id': "str", 
    'seller_zip_code_prefix': "str", 
    'seller_city': "str", 
    'seller_state': "str"
}


ORDER_REVIEWS_PRIMARY_KEY = ["review_id", "order_id"]

ORDER_REVIEWS_COLUMNS = {
    'review_id': "str", 
    'order_id': "str", 
    'review_score': "int", 
    'review_comment_title': "str",
    'review_comment_message': "str", 
    'review_creation_date': "datetime",
    'review_answer_timestamp': "datetime"
}