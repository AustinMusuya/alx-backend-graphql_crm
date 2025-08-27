from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/crm_heartbeat_log.txt"

    # Always log basic heartbeat
    with open(log_file, "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

    # Optional GraphQL hello check (using gql + Client as required)
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("{ hello }")
        result = client.execute(query)

        if "hello" in result:
            with open(log_file, "a") as f:
                f.write(
                    f"{timestamp} GraphQL hello check OK: {result['hello']}\n")
        else:
            with open(log_file, "a") as f:
                f.write(f"{timestamp} GraphQL hello check FAILED\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL hello check ERROR: {e}\n")


def updatelowstock():
    # call the mutation
    mutation = """
    mutation {
        updateLowStockProducts {
            success
            updatedProducts {
                id
                name
                stock
            }
        }
    }
    """

    # log file must be exactly this path
    with open("/tmp/lowstockupdates_log.txt", "a") as log:
        log.write("some log message...\n")
