import os
import time
import boto3
import logging

def logme(message):
    cur_time = time.strftime('%b%e %H:%M:%S', time.localtime())
    logging.basicConfig(filename='system.log', format='%(asctime)s %(message)s', datefmt=str(cur_time), level=logging.INFO)
    logging.info('%s' % message)
    #s3_c = boto3.client('s3', region_name='us-east-2')
    #s3_c.upload_file('system.log', 'ksdevbatcheast2', 'system.log')
    #print('File uploaded to ksdevbatcheast2 system.log')

def main():
    message = 'Log me'
    logme(message)

if __name__ == '__main__':
    main()
