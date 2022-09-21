from PIL import Image
import io
from dotenv import load_dotenv
import os
import boto3
from flask import Flask, request
import base64
import numpy as np
import json

load_dotenv()

# S3_BUCKET = os.environ["S3_BUCKET"]
# AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
# AWS_ACCESS_SECRET = os.environ["AWS_ACCESS_SECRET"]
# S3_LOCATION = "http://{}.s3.amazonaws.com/".format(S3_BUCKET)

# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
#     aws_secret_access_key=os.environ["AWS_ACCESS_SECRET"],
# )

# app = Flask(__name__)

# @app.route('/image', methods=['POST'])
# def image():
#     img = Image.open(request.files['file'])
#     in_mem_file = io.BytesIO()
#     img.save(in_mem_file, format=img.format)
#     in_mem_file.seek(0)

#     try:
#         s3.upload_fileobj(in_mem_file, S3_BUCKET, request.files['file'].filename)
#     except Exception as e:
#         print(str(e))
#     else:
#         data = "{}{}".format(
#             S3_LOCATION, request.files['file'].filename
#         )
#         print(data)
#         return data
    
# if __name__ == '__main__':
#     app.run(debug=True)
    
img = Image.open('aws-credit.png')
# in_mem_file = io.BytesIO()
# img.save(in_mem_file, format=img.format)
# # in_mem_file.seek(0)
# image_as_string = base64.b64encode(in_mem_file.getvalue()).decode('ascii')
# print(type(image_as_string))

# image_as_bytes = base64.b64decode(image_as_string)
# print(type(image_as_bytes))
# img = Image.open(image_as_bytes)
# print(type(img))
json_data = json.dumps(np.array(img).tolist())
new_image = Image.fromarray(np.array(json.loads(json_data), dtype='uint8'))
print(type(new_image))