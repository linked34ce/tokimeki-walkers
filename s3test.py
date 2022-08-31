import boto3
from dotenv import load_dotenv

load_dotenv()
client = boto3.client("s3")

FILENAME = "./static/tmp/op_setsuna.jpg"
BUCKET = "graduation-research"
KEY = "/tmp/yupomu.jpg"

client.upload_file(FILENAME, BUCKET, KEY)