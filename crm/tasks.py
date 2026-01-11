"""
Celery tasks for CRM app.
"""
from celery import shared_task
from django.utils import timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generate_crm_report():
    """
    Generate a weekly CRM report using GraphQL queries.
    Fetches total customers, total orders, and total revenue.
    """
    url = "http://localhost:8000/graphql"
    log_file = '/tmp/crm_report_log.txt'
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create GraphQL client
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    
    try:
        # Query for total customers
        customers_query = gql("""
            query {
                allCustomers {
                    id
                }
            }
        """)
        
        # Query for total orders and revenue
        orders_query = gql("""
            query {
                allOrders {
                    edges {
                        node {
                            id
                            totalAmount
                        }
                    }
                }
            }
        """)
        
        # Execute queries
        customers_result = client.execute(customers_query)
        orders_result = client.execute(orders_query)
        
        # Count customers
        customers = customers_result.get('allCustomers', [])
        total_customers = len(customers)
        
        # Count orders and calculate revenue
        orders_edges = orders_result.get('allOrders', {}).get('edges', [])
        total_orders = len(orders_edges)
        
        # Calculate total revenue
        total_revenue = sum(
            float(edge['node']['totalAmount']) 
            for edge in orders_edges 
            if edge.get('node', {}).get('totalAmount')
        )
        
        # Format revenue
        revenue_str = f"{total_revenue:.2f}"
        
        # Log the report
        report_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {revenue_str} revenue\n"
        with open(log_file, 'a') as f:
            f.write(report_message)
        
        return {
            'customers': total_customers,
            'orders': total_orders,
            'revenue': total_revenue
        }
        
    except Exception as e:
        # Log errors
        error_message = f"{timestamp} - ERROR generating report: {str(e)}\n"
        with open(log_file, 'a') as f:
            f.write(error_message)
        raise
