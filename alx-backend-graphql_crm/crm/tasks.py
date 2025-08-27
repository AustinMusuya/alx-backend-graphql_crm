from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime


@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """)

    result = client.execute(query)
    customers = result.get("customersCount", 0)
    orders = result.get("ordersCount", 0)
    revenue = result.get("totalRevenue", 0)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/crm_report_log.txt", "a") as log:
        log.write(
            f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    return f"Report generated: {customers} customers, {orders} orders, {revenue} revenue"
