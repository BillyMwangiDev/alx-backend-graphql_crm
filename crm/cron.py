"""
Cron jobs for CRM application using django-crontab.
"""
import os
from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Log a heartbeat message every 5 minutes to confirm CRM application health.
    Optionally queries the GraphQL hello field to verify endpoint is responsive.
    """
    timestamp = timezone.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive\n"
    
    # Log to file (append mode)
    log_file = '/tmp/crm_heartbeat_log.txt'
    with open(log_file, 'a') as f:
        f.write(message)
    
    # Optionally query GraphQL hello field (commented out as it requires server to be running)
    # This would verify the GraphQL endpoint is responsive
    # try:
    #     transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    #     client = Client(transport=transport, fetch_schema_from_transport=False)
    #     query = gql("{ hello }")
    #     result = client.execute(query)
    #     with open(log_file, 'a') as f:
    #         f.write(f"{timestamp} GraphQL endpoint responsive: {result.get('hello')}\n")
    # except Exception as e:
    #     with open(log_file, 'a') as f:
    #         f.write(f"{timestamp} GraphQL endpoint check failed: {str(e)}\n")


def update_low_stock():
    """
    Execute the UpdateLowStockProducts mutation via GraphQL endpoint.
    Logs updated product names and new stock levels to /tmp/low_stock_updates_log.txt with timestamp.
    """
    url = "http://localhost:8000/graphql"
    log_file = '/tmp/low_stock_updates_log.txt'
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # GraphQL mutation to update low stock products
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)
    
    try:
        # Create GraphQL client
        transport = RequestsHTTPTransport(url=url)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        
        # Execute mutation
        result = client.execute(mutation)
        
        # Extract results
        mutation_result = result.get('updateLowStockProducts', {})
        updated_products = mutation_result.get('updatedProducts', [])
        message = mutation_result.get('message', '')
        
        # Log to file
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - {message}\n")
            for product in updated_products:
                product_name = product.get('name', 'N/A')
                stock_level = product.get('stock', 'N/A')
                f.write(f"{timestamp} - Updated {product_name} to stock level {stock_level}\n")
        
    except Exception as e:
        # Log errors
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - ERROR: {str(e)}\n")
