# gcp_billing_poc
GCP Billing PoC

## GCP Docs
* https://cloud.google.com/billing/docs/how-to/export-data-bigquery
* https://cloud.google.com/bigquery/docs/running-queries#python
* https://cloud.google.com/bigquery/docs/querying-partitioned-tables
* https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries


## Summary
This Proof of Concept assumes that the user has set their service account credential path using the GOOGLE_APPLICATION_CREDENTIALS environment variable.
It is also assumed that BigQuery billing export has been turned on and is running. The service account logging in also needs access to query the BigQuery billing data. 

We first check permissions using the GCP Resource Manager API
* https://cloud.google.com/resource-manager/
* https://cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions

This is currently stubbed and just prints the resposne from the API. 

We then query a specific billing table and store the result of the query in a CSV file. 

To run main.py add a table name to the TABLE_NAME variable, and a project ID as the argument to check_access().