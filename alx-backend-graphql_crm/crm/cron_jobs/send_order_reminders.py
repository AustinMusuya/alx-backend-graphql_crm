#!/usr/bin/env python3
import sys
import logging
from datetime import datetime, timedelta
import asyncio
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


async def main():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define date range (last 7 days)
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    query = gql("""
    query GetRecentOrders($startDate: Date!, $endDate: Date!) {
        orders(orderDate_Gte: $startDate, orderDate_Lte: $endDate) {
            id
            customer {
                email
            }
        }
    }
    """)

    params = {
        "startDate": str(week_ago),
        "endDate": str(today)
    }

    try:
        result = await client.execute_async(query, variable_values=params)
        orders = result.get("orders", [])

        for order in orders:
            order_id = order["id"]
            customer_email = order["customer"]["email"]
            logging.info(f"Reminder: Order {order_id} for {customer_email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"Error processing reminders: {e}")
        print("Error processing reminders!", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
