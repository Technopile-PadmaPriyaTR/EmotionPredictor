from flask import Flask, render_template, request
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import os
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("Upload.html")

@app.route("/process", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        upload_image = request.files['upload_image']
        print(type(upload_image))
        KEY = "aec15ff556c449488f778af556ac567c"
        ENDPOINT = "https://facialemotion1.cognitiveservices.azure.com//face/v1.0/detect"
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        test_image_array=upload_image
        headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': KEY}
        params = {'returnFaceId': 'true','returnFaceLandmarks': 'true','returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion'}
        response= requests.post(ENDPOINT, params=params, headers=headers, data=test_image_array)
        response.raise_for_status()
        faces = response.json()
        for face in faces:
            fa = face["faceAttributes"]
            emotion = fa["emotion"]
            values = list(emotion.values())
            keys = list(emotion.keys())
            maximum = max(values)
            result = "The emotion of the person is : "+keys[values.index(maximum)]
    return render_template("Name.html", result=result)


@app.route("/Upload")
def back():
    return render_template("Upload.html")

if __name__ == '__main__':
    app.run(debug=True)
