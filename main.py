import boto3
from re import search
from botocore.config import Config

def list_files(client: any, bucket: str, prefix: str = "") -> None:
    # List all files in an S3 Bucket
    response = client.list_objects_v2(Bucket = bucket, Prefix = prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])

def upload_file(client: any, local_path: str, destination_path: str, bucket: str) -> None:
    # Upload a local file to a defined location in the bucket
    client.upload_file(local_path, bucket, destination_path)

def list_files_by_regex(client: any, bucket: str, prefix: str = "", regex_pattern: str = "") -> None:
    # List an AWS buckets files that match a "filter" regex 
    response = client.list_objects_v2(Bucket = bucket, Prefix = prefix)
    if 'Contents' in response:
        matching_patterns = [obj['Key'] for obj in response['Contents'] if search(regex_pattern, obj['Key'])]
        print(matching_patterns)

def delete_files_by_regex(client: any, bucket: str, prefix: str = "", regex_pattern: str = "") -> None:
    response = client.list_objects_v2(Bucket = bucket, Prefix = prefix)
    if 'Contents' in response:
        matching_patterns = [obj['Key'] for obj in response['Contents'] if search(regex_pattern, obj['Key'])]

        if matching_patterns:
            objects_to_delete = [{'Key':file} for file in matching_patterns]

            delete_response = client.delete_objects(
                Bucket = bucket,
                Delete = {'Objects': objects_to_delete}
            )

            deleted = delete_response.get('Deleted', [])
            if deleted:
                print(f"Deleted {len(deleted)} files:")
                for obj in deleted:
                    print(obj['Key'])
        else: print("No files matched given pattern")
    else: print("the bucket is empty or does not exists")

def main() -> None:
    s3 = boto3.client(
        "s3",
    )

    # Task 1

    bucket: str = "developer-task"
    folder: str = 'b-wing'
    list_files(s3, bucket, folder)

    # Task 2

    local_file_path: str = './test_file.txt'
    s3_destination_key: str = 'b-wing/test_file.txt'

    # upload_file(
    #     client= s3,
    #     local_path= local_file_path,
    #     destination_path= s3_destination_key,
    #     bucket= bucket
    # )

    # Task 3

    regex_pattern: str = r"[a-z]+_[a-z]+\.txt"
    # list_files_by_regex(
    #     client=s3,
    #     bucket=bucket,
    #     prefix=folder,
    #     regex_pattern=regex_pattern
    # )

    # Task 4
    # delete_files_by_regex(
    #     client=s3,
    #     bucket=bucket,
    #     prefix=folder,
    #     regex_pattern=regex_pattern
    # )

if __name__ == '__main__':
    main()