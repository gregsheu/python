from PIL import Image
import json
import boto3

img = Image.new('RGB', (1920, 1080), (255, 255, 255))
img.save('/tmp/blank.jpg', 'JPEG')
s3_c = boto3.client('s3')
resp = s3_c.put_object('/tmp/blank.jpg', Bucket='ksdevbatchwest2', 'blank.jpg')
httpstatuscode = resp

def lambda_handler(event, context):
    evt = event['Run']
    return 
    {
        'HTTPStatusCode': json.dumps(httpstatuscode)
    }
