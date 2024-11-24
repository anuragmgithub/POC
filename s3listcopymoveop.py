import boto3

# Specify the bucket name
bucket_name = 'de-stock-market-nifty-data'


# Create an S3 client using the default credential provider chain
s3 = boto3.client('s3')

# List objects (files) in the specified bucket
try:
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Check if there are objects in the bucket
    if 'Contents' in response:
        print(f"Files in '{bucket_name}':")
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print(f"No files found in '{bucket_name}'.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("==========================")


import boto3

# Replace with your AWS credentials and S3 bucket names
source_bucket_name = 'de-stock-market-nifty-data'
destination_bucket_name = 'dp-nifty-data-dest'

# Create an S3 client
s3 = boto3.client('s3')

# List objects (files) in the source bucket
try:
    response = s3.list_objects_v2(Bucket=source_bucket_name)

    # Check if there are objects in the source bucket
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']

            # Check if the object key starts with a letter between 'a' and 'h'
            if key[0] in 'abcdefgh' or key[0] in 'ABCDEFGH':
                # Copy the object to the destination bucket
                copy_source = {'Bucket': source_bucket_name, 'Key': key}
                s3.copy_object(CopySource=copy_source, Bucket=destination_bucket_name, Key=key)

                # Delete the object from the source bucket
                s3.delete_object(Bucket=source_bucket_name, Key=key)

        print("Files starting with 'a' to 'h' have been moved to the destination bucket.")
    else:
        print(f"No files found in '{source_bucket_name}'.")
        print("")

except Exception as e:
    print(f"An error occurred please check... : {e}")
