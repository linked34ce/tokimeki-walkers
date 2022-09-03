import boto3
from dotenv import load_dotenv

load_dotenv()
client = boto3.client("s3")

FILENAME = "./static/images/no_image.jpg"
BUCKET = "tokimeki-walkers"
KEY = "/uploads/no_image.jpg"

client.upload_file(FILENAME, BUCKET, KEY)