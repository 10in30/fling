__version__ = "0.1.3"

from dotenv import load_dotenv
from os import environ
import boto3

load_dotenv()

s3_client = boto3.client('s3')
BUCKET = environ.get("BUCKET", "flingwtf-prod")
REGION = environ.get("REGION", "us-west-2")
DEBUG = environ.get('DEBUG', False)
