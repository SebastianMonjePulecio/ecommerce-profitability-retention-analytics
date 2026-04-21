from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"


def ensure_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def build_customers(rng: np.random.Generator, n_customers: int = 2500) -> pd.DataFrame:
    channels = ["Paid Search", "Organic", "Email", "Affiliate", "Social Ads"]
    regions = ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"]
    signup_dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")

    customers = pd.DataFrame(
        {
            "customer_id": np.arange(1, n_customers + 1),
            "acquisition_channel": rng.choice(channels, size=n_customers, p=[0.28, 0.22, 0.14, 0.12, 0.24]),
            "region": rng.choice(regions, size=n_customers),
            "signup_date": rng.choice(signup_dates, size=n_customers),
        }
    )
    return customers


def build_products() -> pd.DataFrame:
    products = pd.DataFrame(
        {
            "product_id": np.arange(1, 13),
            "category": [
                "Electronics",
                "Electronics",
                "Home",
                "Home",
                "Fashion",
                "Fashion",
                "Beauty",
                "Beauty",
                "Sports",
                "Sports",
                "Accessories",
                "Accessories",
            ],
            "base_price": [420, 650, 120, 220, 80, 140, 35, 55, 190, 260, 20, 45],
            "unit_cost": [280, 430, 70, 130, 34, 62, 11, 17, 108, 148, 7, 15],
        }
    )
    return products


def build_orders(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    n_orders: int = 12000,
) -> pd.DataFrame:
    order_dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    selected_customers = rng.choice(customers["customer_id"], size=n_orders)
    selected_products = rng.choice(products["product_id"], size=n_orders)
    quantity = rng.choice([1, 2, 3], size=n_orders, p=[0.68, 0.24, 0.08])

    base_lookup = products.set_index("product_id")["base_price"]
    channel_lookup = customers.set_index("customer_id")["acquisition_channel"]
    category_lookup = products.set_index("product_id")["category"]

    unit_price = []
    discount_amount = []
    returned_flag = []
    shipping_cost = []

    for customer_id, product_id, qty in zip(selected_customers, selected_products, quantity):
        base_price = float(base_lookup.loc[product_id])
        channel = channel_lookup.loc[customer_id]
        category = category_lookup.loc[product_id]

        discount_rate = 0.0
        if channel in {"Paid Search", "Social Ads"}:
            discount_rate += float(rng.uniform(0.05, 0.18))
        if category in {"Fashion", "Beauty", "Accessories"}:
            discount_rate += float(rng.uniform(0.02, 0.10))
        discount_rate = min(discount_rate, 0.30)

        price = round(base_price * float(rng.uniform(0.92, 1.08)), 2)
        discount = round(price * qty * discount_rate, 2)

        return_probability = 0.05
        if category == "Fashion":
            return_probability = 0.16
        elif category == "Electronics":
            return_probability = 0.09
        elif category == "Accessories":
            return_probability = 0.11

        if channel == "Social Ads":
            return_probability += 0.03

        returned = int(rng.random() < return_probability)
        ship_cost = round(float(rng.uniform(8, 22)), 2)

        unit_price.append(price)
        discount_amount.append(discount)
        returned_flag.append(returned)
        shipping_cost.append(ship_cost)

    orders = pd.DataFrame(
        {
            "order_id": np.arange(1, n_orders + 1),
            "customer_id": selected_customers,
            "product_id": selected_products,
            "order_date": rng.choice(order_dates, size=n_orders),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_amount": discount_amount,
            "shipping_cost": shipping_cost,
            "returned_flag": returned_flag,
        }
    )
    return orders.sort_values("order_date").reset_index(drop=True)


def build_marketing_spend(rng: np.random.Generator) -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    channels = ["Paid Search", "Organic", "Email", "Affiliate", "Social Ads"]
    rows = []

    for spend_date in dates:
        for channel in channels:
            base_spend = {
                "Paid Search": 520,
                "Organic": 80,
                "Email": 140,
                "Affiliate": 200,
                "Social Ads": 430,
            }[channel]
            rows.append(
                {
                    "spend_date": spend_date,
                    "acquisition_channel": channel,
                    "spend": round(float(base_spend * rng.uniform(0.75, 1.35)), 2),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    ensure_directories()
    rng = np.random.default_rng(42)

    customers = build_customers(rng)
    products = build_products()
    orders = build_orders(rng, customers, products)
    marketing_spend = build_marketing_spend(rng)

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    products.to_csv(RAW_DIR / "products.csv", index=False)
    orders.to_csv(RAW_DIR / "orders.csv", index=False)
    marketing_spend.to_csv(RAW_DIR / "marketing_spend.csv", index=False)

    print("Synthetic e-commerce dataset created in data/raw")


if __name__ == "__main__":
    main()

