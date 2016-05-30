#! /usr/bin/env python3
'''
s3sync: synchronize data to AWS S3.
'''
import os
import enum
import argparse

import boto3
import botocore
import pytoml as toml

from libs.config import Config


class BucketAccess(enum.IntEnum):
    Accessible = 0
    NotFound = 404
    Forbidden = 403


class Main():

    def __init__(self, args):
        self.args = args

        self.config = Config()
        self.config.load('s4config.toml')

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


class Initializer():
    '''
    Create the initial s4 directory structure (with the hidden .s4
    directory, configuration details, etc.
    '''

    def __init__(self, args):
        if not os.path.exists(args.path):
            print('The specified path does not exist.')
            exit(1)
        if not os.path.isdir(args.path):
            print('The specified path is not a directory.')
            exit(1)

        print('Creating .s4 directory')
        configdirpath = os.path.join(args.path, '.s4')
        os.mkdir(configdirpath, mode=0o700)

        print('Creating .s4/config.toml')
        configfilepath = os.path.join(configdirpath, 'config.toml')
        config = Config()
        config.save(configfilepath)

        print('Collecting user details')
        response = input('What is your "AWS Access Key ID": ')
        config.config['aws']['credentials']['aws_access_key_id'] = response
        response = input('What is your "AWS Access Key Secret": ')
        config.config['aws']['credentials']['aws_secret_access_key'] = response
        response = input('Name of the sync destination S3 bucket: ')
        config.config['aws']['bucket']['name'] = response
        # TODO: perform validation on the relative path
        response = input('Relative path inside the bucket to sync to: ')
        config.config['aws']['bucket']['path'] = response

        print('Saving .s4/config.toml')
        config.save(configfilepath)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='s4')
    subparsers = parser.add_subparsers()
    parser_init = subparsers.add_parser('init')
    parser_add = subparsers.add_parser('add')

    parser_init.set_defaults(subcommand='init')
    parser_init.add_argument('path', type=str, nargs='?', default='.')

    parser_add.set_defaults(subcommand='init')
    parser_add.add_argument('file', type=argparse.FileType('r'), nargs='+')

    args = parser.parse_args()

    # Launch main class based on subcommand
    if args.subcommand == 'init':
        main = Initializer(args)
    else:
        main = Main(args)
