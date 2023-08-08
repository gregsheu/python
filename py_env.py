import os
import sys
import boto3
def file_from_bucket(s3_bucket, s3_object, region):
    print('Downlading file from %s %s' % (s3_bucket, s3_object))
    s3_c = boto3.client('s3', region_name=region)
    s3_c.download_file(s3_bucket, s3_object, os.path.join(os.curdir, s3_object))
    print('File is downloaded to %s' % os.path.join(os.curdir, s3_object))

def main():
    region = sys.argv[1]
    py_bucket = os.getenv('S3BUCKET')
    py_object = os.getenv('S3OBJECT')
    file_from_bucket(py_bucket, py_object, region)
    exec(open(os.path.join(os.curdir, py_object)).read())

if __name__ == '__main__':
    main()
