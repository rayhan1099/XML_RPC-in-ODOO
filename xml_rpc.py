import xmlrpc.client

# Odoo connection details
url = 'http://localhost:8069'
db = 'new_db'
username = '***'
password = '******'

# XML-RPC endpoints
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Authenticate
uid = common.authenticate(db, username, password, {})

# Check if authentication was successful
if uid:
    print("Authenticated with UID:", uid)
else:
    print("Authentication failed")
    exit()

# Function to find product ID based on SKU
def get_product_id_by_sku(sku):
    product_ids = models.execute_kw(
        db, uid, password,
        'product.product', 'search',
        [[['default_code', '=', sku]]]
    )
    if product_ids:
        return product_ids[0]  # Assuming SKU is unique and returns a single product ID
    else:
        raise ValueError(f"Product with SKU {sku} not found")

# SKU of the product you want to order
sku = 'FURN_6666'  # Replace with the actual SKU

try:
    # Fetch product ID using SKU
    product_id = get_product_id_by_sku(sku)
    
    # Define the Sale Order data
    sale_order_data = {
        'partner_id': 9,  # Replace with the actual partner ID
        'date_order': '2024-09-16',  # Example order date
        'order_line': [
            (0, 0, {
                'product_id': product_id,  # Use product_id here
                'product_uom_qty': 2,  # Quantity
                'price_unit': 100.0,  # Unit price
                'name': 'Product Description',  # Description is now included
            }),
        ],
    }

    # Create the Sale Order
    sale_order_id = models.execute_kw(
        db, uid, password,
        'sale.order', 'create',
        [sale_order_data]
    )

    print("Sale Order Created with ID:", sale_order_id)

    # Fetch Sale Order details for debugging
    sale_order_details = models.execute_kw(
        db, uid, password,
        'sale.order', 'read',
        [sale_order_id],
        {'fields': ['partner_id', 'date_order', 'order_line']}
    )

    # Extract the order line IDs from the Sale Order details
    order_line_ids = sale_order_details[0]['order_line']

    # Fetch detailed Sale Order Line information
    order_line_details = models.execute_kw(
        db, uid, password,
        'sale.order.line', 'read',
        [order_line_ids],
        {'fields': ['product_id', 'product_uom_qty', 'price_unit', 'name']}
    )

    print("Sale Order Details:", sale_order_details)
    print("Sale Order Line Details:", order_line_details)

except ValueError as e:
    print(e)
except Exception as e:
    print("Error:", e)
