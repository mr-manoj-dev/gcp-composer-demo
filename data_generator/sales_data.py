import csv
import random
from datetime import datetime, timedelta

# Number of sales records to generate
num_records = 10000

# Define date range for sales records
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 5, 31)


# Define stationary products
products = ['Pen', 'Pencil', 'Notebook', 'Eraser', 'Stapler', 'Highlighter', 'Scissors', 'Ruler', 'Markers', 'Tape', 'Paper Clips', 'Calculator']

# Create CSV file and write header
csv_file = open('data/sales_records.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['date', 'product_name', 'quantity', 'unit_price', 'total_price'])

# Generate sales records
for _ in range(num_records):
    # Generate a random date within the specified range
    sale_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Choose a random product
    product_name = random.choice(products)
    
    
    # Generate a random quantity and price
    quantity = random.randint(1, 100)
    unit_price = round(random.uniform(1.0, 10.0), 2)
    total_price = round(quantity * unit_price, 2)
    
    # Write the sales record to the CSV file
    csv_writer.writerow([sale_date.strftime('%Y-%m-%d'), product_name, quantity, unit_price, total_price])

# Close the CSV file
csv_file.close()

print(f'{num_records} sales records generated and saved to sales_records.csv.')
