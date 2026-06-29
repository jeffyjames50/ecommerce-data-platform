import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 200
NUM_ORDERS = 5000
NUM_EVENTS = 20000


#Generate Customers
def generate_customers(n):
    customers = []

    for i in range(1, n + 1):
        customers.append({
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "country": fake.country(),
            "city": fake.city(),
            "signup_date": fake.date_between(start_date="-2y", end_date="today")
        })

    return pd.DataFrame(customers)


#Generate Products
def generate_products(n):
    categories = ["Beverages", "Snacks", "Dairy", "Personal Care", "Household"]

    products = []

    for i in range(1, n + 1):
        products.append({
            "product_id": i,
            "product_name": fake.word().capitalize(),
            "category": random.choice(categories),
            "brand": fake.company(),
            "unit_price": round(random.uniform(1, 100), 2)
        })

    return pd.DataFrame(products)

#Generate Orders
def generate_orders(n, num_customers):
    orders = []

    for i in range(1, n + 1):
        orders.append({
            "order_id": i,
            "customer_id": random.randint(1, num_customers),
            "order_date": fake.date_between(start_date="-1y", end_date="today"),
            "order_status": random.choice(["completed", "cancelled", "returned"]),
            "total_amount": round(random.uniform(10, 500), 2)
        })

    return pd.DataFrame(orders)

#order items generator
def generate_order_items(orders_df, products_df):
    order_items = []
    item_id = 1

    for _, order in orders_df.iterrows():
        num_items = random.randint(1, 5)

        for _ in range(num_items):
            product = products_df.sample(1).iloc[0]

            quantity = random.randint(1, 3)

            order_items.append({
                "order_item_id": item_id,
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": product["unit_price"]
            })

            item_id += 1

    return pd.DataFrame(order_items)


#user events generator
def generate_user_events(customers_df, products_df, n_events):
    events = []
    event_types = ["view", "click", "add_to_cart", "purchase"]

    for i in range(1, n_events + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]

        events.append({
            "event_id": i,
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "event_type": random.choice(event_types),
            "event_timestamp": fake.date_time_between(start_date="-6M", end_date="now")
        })

    return pd.DataFrame(events)

#main function
if __name__ == "__main__":

    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    orders = generate_orders(NUM_ORDERS, NUM_CUSTOMERS)

    order_items = generate_order_items(orders, products)
    user_events = generate_user_events(customers, products, NUM_EVENTS)

    customers.to_csv("data/raw/customers.csv", index=False)
    products.to_csv("data/raw/products.csv", index=False)
    orders.to_csv("data/raw/orders.csv", index=False)
    order_items.to_csv("data/raw/order_items.csv", index=False)
    user_events.to_csv("data/raw/user_events.csv", index=False)

    print("Data generation complete!")