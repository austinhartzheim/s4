#! /usr/bin/env python3
'''
s3sync: synchronize data to AWS S3.
'''
import os

import boto3
import botocore
import pytoml as toml


def sync(config):
    for root, dirs, files in os.walk(config['sync']['root']['path']):
        # TODO: add code to ignore the s4 config to avoid syncing credentials
        print('%s:' % root)
        for dire in dirs: print('  d %s' % dire)
        for file in files: print('  f %s' % file)


if __name__ == '__main__':
    # Load configuration file
    import pprint
    with open('s4config.toml') as config_f:
        config = toml.load(config_f)
    pprint.pprint(config)  # TODO: remove debug

    # Create AWS session
    session = boto3.session.Session(**config['aws']['credentials'])
    s3 = session.resource('s3')

    # Check if bucket exists
    try:
        s3.meta.client.head_bucket(Bucket=config['aws']['bucket']['name'])
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

    # Sync files
    sync(config)
