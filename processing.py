from google.cloud import vision
import io
from PIL import Image
import numpy as np

client = vision.ImageAnnotatorClient()


def face_sentiment(frame):
    """Detects sentiment from face in an image. reterns string with sentiment"""

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
