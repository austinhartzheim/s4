#! /usr/bin/env python3
'''
s3sync: synchronize data to AWS S3.
'''
import os
import enum

import boto3
import botocore
import pytoml as toml


class BucketAccess(enum.IntEnum):
    Accessible = 0
    NotFound = 404
    Forbidden = 403


class Main():

    def __init__(self):
        self.config = self.load_config()
        session = boto3.session.Session(**self.config['aws']['credentials'])
        self.s3 = session.resource('s3')

        # Check if bucket exists
        check = self.check_bucket_access(self.config['aws']['bucket']['name'])
        if check == BucketAccess.NotFound:
            print('Configured bucket does not exist.')
            exit(1)
        elif check == BucketAccess.Forbidden:
            print('Error: do not have permission to access configured bucket')
            print('The following are some known causes of this error:')
            print(' - User does not have access to S3')
            print(' - The bucket is owned by another account')
            exit(1)

        # Sync files
        self.sync()

    def sync(self):
        for root, dirs, files in os.walk(self.config['sync']['root']['path']):
            # TODO: add code to ignore any s4 configuration files
            print('%s:' % root)
            for dire in dirs: print('  d %s' % dire)
            for file in files: print('  f %s' % file)

    def load_config(self):
        '''
        Find and load the configuration file.
        '''
        import pprint
        with open('s4config.toml') as config_f:
            config = toml.load(config_f)
        pprint.pprint(config)  # TODO: remove debug
        return config

    def check_bucket_access(self, bucketname):
        '''
        Check if a bucket with the specified name exists.
        :param str bucketname: the name of the bucket to check.
        :returns bool: true - if the bucket exists, false otherwise.
        '''
        try:
            self.s3.meta.client.head_bucket(Bucket=bucketname)
            return BucketAccess.Accessible
        except botocore.exceptions.ClientError as err:
            error_code = int(err.response['Error']['Code'])
            if error_code in BucketAccess:
                return error_code
            else:
                raise err


if __name__ == '__main__':
    main = Main()
