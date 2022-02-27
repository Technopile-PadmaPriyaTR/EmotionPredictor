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
        KEY = "aec15ff556c449488f778af556ac567c"
        ENDPOINT = "https://facialemotion1.cognitiveservices.azure.com//face/v1.0/detect"
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        image_stream=open(upload_image.filename,"rb")
        #single_image_name = os.path.basename(upload_image)
        headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': KEY}
        params = {'returnFaceId': 'true','returnFaceLandmarks': 'true','returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion'}
        response= requests.post(ENDPOINT, params=params, headers=headers, data=image_stream)
        response.raise_for_status()
        faces = response.json()
        image_orig = open(upload_image.filename, "rb").read()
        img = Image.open(BytesIO(image_orig))
        draw = ImageDraw.Draw(img)
        for face in faces:
            fa = face["faceAttributes"]
            emotion = fa["emotion"]
            values = list(emotion.values())
            keys = list(emotion.keys())
            maximum = max(values)
            result = "Emotion: " + keys[values.index(maximum)]
            draw.rectangle(getRectangle(face), outline='red')
            font = ImageFont.truetype("arial.ttf", 30, )
            draw.text((getRectangle(face)[0], getRectangle(face)[1]), result, "white", font=font, weight="bold")
            img.show()
        return render_template("Upload.html")

#@app.route("/Upload")
def getRectangle(faceDictionary):
    rect = faceDictionary["faceRectangle"]
    left = rect["left"]
    top = rect["top"]
    right = left + rect["width"]
    bottom = top + rect["height"]
    return ((left), (top),(right),(bottom))
    #return render_template("Upload.html")


if __name__ == '__main__':
    app.run(debug=True)
