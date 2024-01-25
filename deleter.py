import boto3

def list_unused_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    unused_buckets = []

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        # Check if the bucket is empty
        try:
            s3.list_objects(Bucket=bucket_name)
        except s3.exceptions.NoSuchBucket:
            # If NoSuchBucket exception is raised, the bucket does not exist
            unused_buckets.append(bucket_name)
        except s3.exceptions.ClientError as e:
            # If Access Denied exception is raised, we assume the bucket is not empty
            if e.response['Error']['Code'] == 'AccessDenied':
                unused_buckets.append(bucket_name)

    return unused_buckets

def delete_buckets(bucket_names):
    s3 = boto3.client('s3')

    for bucket_name in bucket_names:
        try:
            s3.delete_bucket(Bucket=bucket_name)
            print(f"Deleted bucket: {bucket_name}")
        except s3.exceptions.ClientError as e:
            print(f"Error deleting bucket {bucket_name}: {e}")

if __name__ == "__main__":
    unused_buckets = list_unused_buckets()

    if unused_buckets:
        print("Unused Buckets:")
        for bucket in unused_buckets:
            print(bucket)

        confirmation = input("Do you want to delete these buckets? (yes/no): ").lower()
        if confirmation == 'yes':
            delete_buckets(unused_buckets)
    else:
        print("No unused buckets found.")
