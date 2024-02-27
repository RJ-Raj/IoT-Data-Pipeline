
# IOT Data Pipeline

This repository contains the implementation of an IoT data pipeline designed to ingest, process, and store IoT device data using Azure services. The pipeline leverages Azure Data Factory (ADF), Azure Data Lake Storage (ADLS), Azure Functions, and Azure SQL Database.




## Pre-requisites
* Azure account
* AWS account
* Knowledge of Storage in Cloud, Azure Data Factory(ADF)



## Architecture
The IoT data pipeline consists of the following steps:

Copy Data from AWS S3 to Azure Data Lake Storage (ADLS):
* Utilize Azure Data Factory (ADF) copy activity to transfer the IoT data file from an AWS S3 bucket to ADLS.
* Schedule this copy activity to run nightly to ensure the latest data is available for processing.
  
Validate and Process Data Using Azure Functions:
* Set up an Azure Function with a blob trigger to monitor the arrival of new data in the ADLS source container.
* Validate the incoming JSON files to ensure they are formatted correctly.
* If the JSON file is valid, use the Azure Storage Blob service client to copy the file into the sink container. Otherwise, move it to the rejected container.
  
Trigger SQL Copy Job:
* Once a valid JSON file is landed in the sink container, initiate a SQL copy job using a blob storage trigger in ADF.
* This job will transfer the data from the sink container to an Azure SQL Database for further analysis and reporting.
## Implementation

Azure Data Lake Storage (ADLS):

* Create an ADLS instance with Hot tier for storing incoming data. Enabling the namespace heirarchy while creating storage account.
* Create three containers -> source, sink, rejected.

Azure Key Vault:

* Create an Azure Key Vault to securely store sensitive information.
* Add RBAC role of Key Vault administrator for the root user.
* Create secrets for S3AccessKeyId and S3SecretKey.
* Assign the "Key Vault Secrets User" role assignment to ADF resource in Access control RBAC.
  
Azure Functions:

* Install Azure Core Tools on your PC.
* Set up a virtual environment and install necessary packages like azure-storage-blob and azure-functions.
* Add Azure Function, Azure Account, and Azure Resources extensions in Visual Studio Code.
* Create a Function App.
* Create an Azure Function with a blob trigger to monitor the source container in ADLS.
* Implement validation logic for incoming JSON files.
* Use the Azure Storage Blob service client to copy valid files to the sink container and move invalid files to the rejected container.
* Test locally using "func start" command in the terminal.
* Deploy the function to the Function App.
* Publish the Function App to Azure using "func azure functionapp publish <functionappname>".
* Add Connection String of the ADLS to the Function App configuration under Application Settings.
  
ADF Configuration:

* In ADF, create linked services for Key Vault, S3, and ADLS.
* Create datasets for S3 and ADLS with parameters for date-type directory structure.
* Create a copy activity to move data from the S3 bucket to ADLS.
* Debug and test the copy activity.
* Schedule the copy activity to run nightly or as per your requirements.
  
Azure SQL Database:
* Set up an Azure SQL Database to store the processed IoT data.
* Configure a SQL copy job in ADF triggered by a blob storage trigger to transfer data from the sink container to the SQL Database.
  
Testing and Deployment:

* Test the pipeline thoroughly to ensure all components are functioning correctly.
* Deploy the pipeline to your Azure environment.

Notes:

* Ensure proper access control and permissions are set up for AWS S3, Azure Key Vault, ADLS, and Azure SQL resources.
* Regularly monitor and manage storage to optimize costs and performance.
* Implement logging and monitoring to track data movement and pipeline performance.
* Follow best practices for security, data governance, and compliance throughout the pipeline
