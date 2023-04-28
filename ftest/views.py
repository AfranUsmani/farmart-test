from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
import boto3
import uuid
import os
import pymongo
from io import BytesIO
import requests
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.getenv("AWS_STORAGE_BUCKET_NAME")

s3 = boto3.client('s3', region_name='ap-south-1', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, config=boto3.session.Config(signature_version='s3v4'))
s3_region = 'ap-south-1'

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['file_uploader']


@csrf_exempt
def upload_file(request):
    if request.method == 'PUT':
        # Get file from request
        file = BytesIO(request.body)
        # Generate unique filename
        filename = request.META.get('HTTP_X_FILE_NAME', 'unknown')+os.path.splitext(request.content_type)[1]
        # Upload file to S3
        s3.upload_fileobj(file, 'farmart-test', filename)

        bucket_name = AWS_STORAGE_BUCKET_NAME
        key = filename
        file_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600 # Time in seconds
        )
        
        # Generate shortened URL
        url = "https://url-shortener-service.p.rapidapi.com/shorten"
        payload = { "url":file_url}
        headers={
            "content-type": "application/x-www-form-urlencoded",
	    "X-RapidAPI-Key": "ef90b60d4fmsh20ced767fb4ba0dp19b5e0jsnc6bcf49b0b98",
	    "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
        }
        response = requests.post(url, data=payload, headers=headers)
        respJson=response.json()
        
        short_url = respJson['result_url']
        # Store short URL in MongoDB
        db.urls.insert_one({'url': short_url, 'filename': filename,'S3url':file_url})
        # Return short URL to client
        return JsonResponse({'url': short_url, 'file_url': file_url, 'filename':filename})
    else:
        return JsonResponse({'error': 'Invalid request method.'})