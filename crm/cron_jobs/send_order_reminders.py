#!/usr/bin/env python
"""
Script to send order reminders for pending orders (order_date within last 7 days).
Uses GraphQL to query orders and logs reminders.
"""
import os
import sys
import django
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from django.utils import timezone


def send_order_reminders():
    """Query GraphQL for orders within last 7 days and log reminders."""
    # GraphQL endpoint
    url = "http://localhost:8000/graphql"
    
    # Create GraphQL client
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    
    # Calculate date 7 days ago
    seven_days_ago = timezone.now() - timedelta(days=7)
    date_str = seven_days_ago.isoformat()
    
    # GraphQL query to get orders within last 7 days
    # Using orderDateGte filter (camelCase version of order_date_gte)
    query = gql("""
        query GetRecentOrders($orderDateGte: DateTime!) {
            allOrders(orderDateGte: $orderDateGte) {
                edges {
                    node {
                        id
                        orderDate
                        customer {
                            email
                        }
                    }
                }
            }
        }
    """)
    
    try:
        # Execute query
        result = client.execute(query, variable_values={"orderDateGte": date_str})
        
        # Process results
        orders = result.get('allOrders', {}).get('edges', [])
        
        # Log to file
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - Processing {len(orders)} order reminders\n")
            
            for edge in orders:
                node = edge.get('node', {})
                order_id = node.get('id', 'N/A')
                customer = node.get('customer', {})
                email = customer.get('email', 'N/A')
                f.write(f"{timestamp} - Order ID: {order_id}, Customer Email: {email}\n")
        
        print("Order reminders processed!")
        
    except Exception as e:
        # Log errors
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - ERROR: {str(e)}\n")
        print(f"Error processing order reminders: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    send_order_reminders()
