import csv
import datetime

import google.auth
from google.cloud import bigquery
from googleapiclient import discovery

# BigQuery specifies the table name in the format projectID:dataset.tableID
# To query we need to replace the : with a ,
# i.e. projectID.dataset.tableID


def check_access(project):
    """Check that we have been granted the required permissions in the project."""
    credentials, project = google.auth.default()
    service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

    check_permissions = {
        "permissions": [
            "bigquery.jobs.create",
            "bigquery.tables.getData",
            "bigquery.tables.list",
            "bigquery.tables.get"
        ]
    }

    request = service.projects().testIamPermissions(resource=project, body=check_permissions)
    response = request.execute()
    print(f"Checking for permissions in project {project}")
    # We would want to check the response to make sure our required permissions are in the response
    print(response)


def get_table_id(data_set):
    """Get the billing table from a dataset in the format projectID.dataset"""
    print(f"Getting table ID for dataset {data_set}")
    client = bigquery.Client()
    for table in client.list_tables(data_set):
        if "gcp_billing_export" in table.full_table_id:
            table_id = table.full_table_id.replace(":", ".")
            print(f"Table ID: {table_id}")
            return table_id
    return None


def get_last_modified(table_id):
    """Get the last modified date for the table."""
    client = bigquery.Client()
    billing_table = client.get_table(table_id)
    last_modified = billing_table.modified
    print(f"Table last modified: {last_modified}")
    return last_modified


def query_table(table_id):
    """Query BigQuery cost data and store in CSV."""
    query_date = datetime.datetime.utcnow().date() - datetime.timedelta(days=600)
    client = bigquery.Client()

    query = f"""
        SELECT billing_account_id,
            service.id,
            service.description,
            sku.id,
            sku.description,
            usage_start_time,
            usage_end_time,
            project.id,
            project.name,
            project.labels,
            project.ancestry_numbers,
            labels,
            system_labels,
            location.location,
            location.country,
            location.region,
            location.zone,
            export_time,
            cost,
            currency,
            currency_conversion_rate,
            usage.amount,
            usage.unit,
            usage.amount_in_pricing_units,
            usage.pricing_unit,
            credits,
            invoice.month,
            cost_type
        FROM {table_id}
        WHERE DATE(_PARTITIONTIME) >= '{query_date}'
    """

    query_job = client.query(query)

    with open("results.csv", "w") as f:
        writer = csv.writer(f)
        for row in query_job:
            writer.writerow(row)
    print("Wrote query results to file.")


if __name__ == "__main__":
    check_access("")  # Add project ID
    table_id = get_table_id("")  # Add projectID.dataset
    get_last_modified(table_id)
    query_table(table_id)

