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







Brainstorming:
- GAN to make vid chat higher quality
- AR in vid chat with retro-themed popups
- make vid chat less boring
- reminders to move around
- eye tracking to see if you are paying attention

Inspiration:
- [avatarify](https://github.com/alievk/avatarify)
  - make a virtual camera to interface with Zoom

## Product Description
 - Marketing:
   - marketed as retro-zoom
   - marketed as an extension to zoom, but really its 3rd party application
   - "An interactive Zoom tool that promotes engagement and prevents Zoom fatigue"
 - Features:
   - self monitor for productiveness (Carly - retro filter, coin update in coin grab game)
      - mario pipeline fills when you pay attention and are happy
      - get coins each time pipeline is complete
      - displayed through zoom camera
      - reports send to db and displayed in ui
   - popups (Shiv/Nilai - data analytics - stacked hist, seeing group emotion over time)
      - prompted by long periods of high sad, low joy emotions (tracked in bg, not notified, presented in summary)
      - prompted by eye tracker sensing long periods of wandering (difficult to implement, perhaps not accurate indicator of productivity)
      - prompted by time limit set to daily value (store value in file to track time during day, sound or popup)
   - games (Nilai - object find - what labels? game logic implementation) (Jack - asteroid game - then data analytics w shiv)
      - coin collect
        - move your head around to collect bags of coins. 
        - coins explode in cool gravity fashion when collected
      - object find
        - prompt you to find an object, must present it to the camera
        - apple, banana, tv remote, phone, can, etc. 
        - coin animation for getting an item correct
      - flappy bird
        - flappy bird but your head/nose is the bird and you have to move your head to direct it
        - count obstacles gone through
      - astroid dodge
        - dodge the astroids coming from offscreen with head

