__version__ = "0.1.4"

from dotenv import load_dotenv
from os import environ
import boto3

load_dotenv()

s3_client = boto3.client('s3')
r53 = boto3.client("route53")
BUCKET = environ.get("BUCKET", "flingwtf-prod")
REGION = environ.get("REGION", "us-west-2")
DEBUG = environ.get('DEBUG', False)
SSH_KEY = environ.get('SSH_KEY')
SSH_USERNAME = environ.get('SSH_USERNAME', 'joshuamckenty')
