import boto3
from botocore.config import Config

def list_files(client: any, bucket: str, prefix: str = "") -> None:
    # List all files in an S3 Bucket
    response = client.list_objects_v2(Bucket = bucket, Prefix = prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])

def upload_file(client: any, local_path: str, destination_path: str, bucket: str):
    client.upload_file(local_path, bucket, destination_path)

def main() -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id = "access_key_id",
        aws_secret_access_key = "access_key"
    )
    bucket: str = "developer-task"
    folder: str = 'b-wing'

    list_files(s3, bucket, folder)

    # Upload a local file to a defined location in the bucket
    local_file_path: str = './test_file.txt'
    s3_destination_key: str = 'b-wing/test_file.txt'

    upload_file(
        client= s3,
        local_path= local_file_path,
        destination_path= s3_destination_key,
        bucket= bucket
    )

if __name__ == '__main__':
    main()