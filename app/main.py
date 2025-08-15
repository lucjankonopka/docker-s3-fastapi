import boto3
import json
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Load .env only locally (no injected variables)
if not os.getenv("AWS_REGION"):
    load_dotenv()

app = FastAPI()

AWS_PROFILE = os.getenv("AWS_PROFILE")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")

key = "input/sample2.json"

@app.get("/data")
def get_data():
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return json.loads(obj["Body"].read())
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            raise HTTPException(status_code=404, detail="File not found")
        else:
            raise HTTPException(status_code=500, detail="S3 error")


@app.get("/")
def root():
    return {"message": "Data API is running!"}
