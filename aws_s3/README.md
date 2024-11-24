# S3 Bucket File Operations

This repository contains Python programs that demonstrate basic file operations on Amazon S3 buckets using the Boto3 library.

### List S3 Files

### Summary

The `s3listcopymoveop.py` program connects to an Amazon S3 bucket and lists all the files within it. It utilizes the Boto3 library to interact with AWS services.

### Usage

1. Ensure you have Boto3 installed: `pip install boto3`.
2. Replace `'YOUR_ACCESS_KEY_ID'`, `'YOUR_SECRET_ACCESS_KEY'`, and `'your-s3-bucket-name'` in the program with your AWS access credentials and the name of the S3 bucket you want to list files from.
3. Run the program to list the files in the specified bucket

## Move S3 Files

### Summary

The `s3listcopymoveop.py` program connects to an Amazon S3 bucket, identifies files starting with names from 'a' to 'h', and moves them to another S3 bucket. It uses the Boto3 library for AWS interaction..

### Usage

1. Ensure you have Boto3 installed: `pip install boto3`.
2. Replace `'source-bucket-name'` and `'destination-bucket-name'` in the program with the names of your source and destination S3 buckets, respectively.
3. Run the program to move files from the source to the destination bucket based on the specified criteria.

Please make sure you have the necessary AWS credentials and IAM permissions set up to perform these operations.