import io
import os

import cv2
import numpy as np
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vandy-hacks-2020-a026305d4125.json'
from google.cloud import vision

client = vision.ImageAnnotatorClient()
faceCascade = cv2.CascadeClassifier('face_detection.xml')


def face_sentiment(frame):
    """Detects sentiment from face in an image. returns string with sentiment"""

    ## Convert to an image, then write to a buffer.
    image_from_frame = Image.fromarray(np.uint8(frame))
    buffer = io.BytesIO()
    image_from_frame.save(buffer, format='PNG')
    buffer.seek(0)

    ## Use the buffer like a file.
    content = buffer.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    if faces:

        # get first face
        face = faces[0]

        # score emotions of the face
        emotions = {'anger': int(face.anger_likelihood),
                    'joy': int(face.joy_likelihood),
                    'surprise': int(face.surprise_likelihood),
                    'sorrow': int(face.sorrow_likelihood)}

        # select most prominent emotion
        most_expressed_emotion = max(emotions, key=emotions.get)
    else:
        most_expressed_emotion = ''

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return most_expressed_emotion


def face_detection(frame):
    """ detect face using cv2

    :param frame:
    :return: (x,y), w, h: face position x,y coordinates, face width, face height
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    position_x, position_y ,width,height = 0, 0, 0, 0
    for x, y, w, h in faces:
        position_x, position_y ,width,height = x, y, w, h

    return position_x, position_y,width,height
