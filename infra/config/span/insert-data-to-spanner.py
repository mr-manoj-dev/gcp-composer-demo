from google.cloud import spanner
import uuid

# Initialize a Spanner client
spanner_client = spanner.Client()

# Define your Spanner instance and database
instance_id = 'span-demo-01'
database_id = 'demo-db-01'

# Create a Spanner instance and database object
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# Generate 100 unique product names using UUID
unique_products = [
    {
        'product_id': i + 1,
        'product_name': f'Product_{i + 1}',
        'product_description': f'Description of Product {i + 1}'
    }
    for i in range(100,200)
]



# Begin a transaction
# Begin a transaction
with database.batch() as batch:
  # Iterate through the unique products and insert them
  for product in unique_products:
    columns = ['product_id', 'product_name', 'product_description']
    values = (product['product_id'], product['product_name'], product['product_description'])
    batch.insert(table='products', columns=columns, values=[values])

# Close the database
spanner_client.close()



# virtualenv span-venv
# source span-venv/bin/activate 
# pip install google-cloud-spanner
# python insert-data-to-spanner.py


# CREATE TABLE products (
#   product_id INT64 NOT NULL,
#   product_name STRING(255),
#   product_description STRING(MAX),
# ) PRIMARY KEY (product_id);
