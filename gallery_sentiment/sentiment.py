import io
import os

import numpy as np
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../vandy-hacks-2020-a026305d4125.json'
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def face_sentiment(frame):
    """Detects sentiment from face in an image. returns string with sentiment"""

    # initial function call with multithreading won't have a frame
    if frame is None:
        return ''

    # Convert to an image, then write to a buffer.
    image_from_frame = Image.fromarray(np.uint8(frame))
    buffer = io.BytesIO()
    image_from_frame.save(buffer, format='PNG')
    buffer.seek(0)

    # Use the buffer like a file.
    content = buffer.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    emotions = [0]*4  # 4 member list of zeros to store emotions
    # weights for these values: ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    weighted_values = [0, 0, 0.25, 0.5, 0.75, 1]
    print(len(faces))
    for face in faces:
        emotions[0] += weighted_values[face.anger_likelihood] * face.detection_confidence
        emotions[1] += weighted_values[face.joy_likelihood] * face.detection_confidence
        emotions[2] += weighted_values[face.surprise_likelihood] * face.detection_confidence
        emotions[3] += weighted_values[face.sorrow_likelihood] * face.detection_confidence

    total = sum(emotions)
    if total: # if not divide by zero
        emotions = [emotions[i] / total for i in range(len(emotions))]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return emotions


