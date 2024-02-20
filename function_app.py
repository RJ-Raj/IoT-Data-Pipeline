import azure.functions as func
import json
import logging
from azure.storage.blob import BlobServiceClient as bsc

app = func.FunctionApp()

@app.function_name("BlobTrigger1")
@app.blob_trigger("myblob", "source/{name}", connection="connString")
def test_function(myblob: func.InputStream):
    logging.info("Python blob trigger function processed blob\n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    connString = "DefaultEndpointsProtocol=https;AccountName=stvehicles0001;AccountKey=4660ml3GpprDJ9t4ZB0Uao5AEDCDEWSCxq5oEzQV+K2mOdmyp3aYkCmu2+/zEGQVJDkQBWJJOUK1+AStZ5xnZA==;EndpointSuffix=core.windows.net"
    blobserviceclient = bsc.from_connection_string(connString)
    filepatharray = myblob.name.split("/")
    sourcefilename = "/".join(filepatharray[1:])
    logging.info(f"File Name is : {sourcefilename}")
    destcontainer = ""
    try:
        blob = myblob.read()
        json_data = json.loads(blob)
        if(json_data):
            destcontainer = "sink"
        else:
            destcontainer = "rejected"
            logging.info(f"This is rejected file.")
        blob_client = blobserviceclient.get_blob_client(container=destcontainer,blob=sourcefilename)
        blob_client.upload_blob(blob)
        logging.info(f"Blob Copied to {destcontainer}/{sourcefilename}")
    except Exception as e:
        destcontainer = "rejected"
        blob_client = blobserviceclient.get_blob_client(container=destcontainer,blob=sourcefilename)
        blob_client.upload_blob(blob)
        logging.info(f"This file is Rejected. Blob Copied to {destcontainer}/{sourcefilename}")
        logging.error(f"An error occurred: {e}")
