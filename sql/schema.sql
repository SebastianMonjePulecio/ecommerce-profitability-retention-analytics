CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    acquisition_channel TEXT,
    region TEXT,
    signup_date DATE
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category TEXT,
    base_price NUMERIC,
    unit_cost NUMERIC
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    unit_price NUMERIC,
    discount_amount NUMERIC,
    shipping_cost NUMERIC,
    returned_flag INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE marketing_spend (
    spend_date DATE,
    acquisition_channel TEXT,
    spend NUMERIC
);

