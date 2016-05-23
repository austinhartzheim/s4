#! /usr/bin/env python3
'''
s3sync: synchronize data to AWS S3.
'''
import boto3
import botocore
import pytoml as toml


if __name__ == '__main__':
    # Load configuration file
    import pprint
    with open('s4config.toml') as config_f:
        config = toml.load(config_f)
    pprint.pprint(config)  # TODO: remove debug

    # Create AWS session
    session = boto3.session.Session(
        aws_access_key_id=config['credentials']['access_key_id'],
        aws_secret_access_key=config['credentials']['access_key_secret'])
    s3 = session.resource('s3')

    # Check if bucket exists
    try:
        s3.meta.client.head_bucket(Bucket=config['credentials']['bucket'])
    except botocore.exceptions.ClientError as err:
        error_code = int(err.response['Error']['Code'])
        if error_code == 404:  # Bucket could not be found
            # TODO: ask if bucket should be created
            print('Configured bucket does not exist.')
            exit(1)
        elif error_code == 403:
            print('Error: do not have permission to access configured bucket')
            print('The following are some known causes of this error:')
            print(' - User does not have access to S3')
            print(' - The bucket is owned by another account')
