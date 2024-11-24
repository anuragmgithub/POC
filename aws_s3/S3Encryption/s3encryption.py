import boto3

# Replace with your AWS credentials and S3 bucket name

bucket_name = 'dp-aws-s3-op'
file_path = 'F:/sampledata/archive/CIPLA.csv'


# Create an S3 client
s3 = boto3.client('s3')

# Specify server-side encryption option
s3.put_object(
    Bucket=bucket_name,
    Key='CIPLA.csv',
    Body=open(file_path, 'rb'),
    ServerSideEncryption='AES256'  # Use SSE-S3 for encryption this is default for the bucket
)

print("Sensitive data uploaded to S3 with server-side encryption (SSE-S3).")
