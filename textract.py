import boto3
import time
import streamlit as st
import os

def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        })

    return response["JobId"]


def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    #st.write("Job status: {}".format(status))


    placeholder = st.subheader(f"Processing...")
    process_bar = st.progress(0)
    while (status == "IN_PROGRESS"):
        for percent_complete in range(100):
            #time.sleep(5)
            time.sleep(0.1)
            response = client.get_document_text_detection(JobId=jobId)
            print(response)
            status = response["JobStatus"]
            #st.write("Job status: {}".format(status))
            process_bar.progress(percent_complete + 1)
    return status


def getJobResults(jobId):
    pages = []

    time.sleep(5)

    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)

    pages.append(response)
    st.write("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if ('NextToken' in response):
        nextToken = response['NextToken']

    while (nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if ('NextToken' in response):
            nextToken = response['NextToken']

    return pages

def uplode_file_to_S3(s3BucketName, objectName, path):
    print(f'uploading {file_name} to s3')
    #path = '/Users/andersmarstrand/Documents/GitHub/lonseddel_kontrol/'
    s3 = boto3.resource('s3')
    s3.Bucket(s3BucketName).upload_file(path + file_name, file_name)

def file_selector(folder_path):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(selected_filename)


# Picked path, file and s3 bucket
st.title("Extract text with AWS rekogniton text extraction")
path = st.text_input('Insert file path here:', os.environ['HOME'] + '/Desktop/')
s3BucketName = "textract-console-us-east-2-93670593-4169-4d03-883c-b1e56ed9e822"

if path is not st.empty():
    file_name = file_selector(path)
    #st.write('You selected `%s`' % file_name)
    if file_name is not None:
        if st.button("Process with AWS Textract"):
            placeholder = st.empty()

            # If file isn't in s3
            #st.write(path)
            uplode_file_to_S3(s3BucketName, file_name, path)

            # Start processing file
            jobId = startJob(s3BucketName, file_name)
            #st.text("Started job with id: {}".format(jobId))
            if (isJobComplete(jobId)):
                response = getJobResults(jobId)

            #st.write(response)

            # Print detected text
            for resultPage in response:
                for item in resultPage["Blocks"]:
                    if item["BlockType"] == "LINE":
                        if item["Confidence"] > 70:
                            # Confidence above 70%
                            st.write(item["Text"])

                        else:
                            # Confidence below 70%
                            st.write(item["Text"] + ' (' + str(item["Confidence"]) + ')')
else:
    st.write('Select a file')