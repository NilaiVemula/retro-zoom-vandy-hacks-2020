import cv2

from google.cloud import vision
import io
from PIL import Image
import numpy as np

client = vision.ImageAnnotatorClient()


# take in a frame. Call the google bision api and return the emotions of each face
def get_emotion(frame):

    print('ok')

    if frame is None:
        return None

    """Detects faces in an image."""

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

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    #print('Faces:')
    face_position = (0,0)
    for face in faces:
        #print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in face.bounding_poly.vertices])

        vertex = face.bounding_poly.vertices[0]
        face_position = vertex.x, vertex.y

        #print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return faces
    

faceCascade = cv2.CascadeClassifier('face_detection.xml')


def face_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return faces