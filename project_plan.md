# Plan for VandyHacks!

## Project breakdown:

1. Capture webcam in python 
2. Modify video stream
    - Google cloud API (getting data from frame)
    - Overlaying images on the frame
        - Time based pop-ups (factory pattern)
            - Too much time
            - You look sad
            - Pay attention!
        - AR environment
            - Super mario styled - grab gold coins
            - Image editing in GIM (Jack)
            - Overlay pixelated filter
3. Game logic
    - Integrated with video
    - Controlled with emotions or head movement
    - Mask RCNN
    - Box to track head like snap cam git
    - Retro style
4. Stream to virtual camera

## Project Structure:

- Class based structure: (Everything runs in infinite loop)
    - Get frame from webcam
    - Send to process frame fn
        - Makes decision on what to do with state
        - Updates state
        - Return new frame with overlay
    - Get frame frome fn and send to virtual camera

- **State diagram**
    - Control object that maintains state
    - Start method begins infinite loop

## Roles:

- Jack:     debugging for (1)
- Nilai:    face detection (2)
- Carly:    Google cloud API research (2) 
