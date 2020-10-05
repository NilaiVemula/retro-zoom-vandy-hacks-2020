# Retro Zoom (Vandy Hacks VII - 10/4/2020)

<div valign="bottom">

<img src="assets/zoom-icon.png" width="33%" align="right" valign="top">

**Description**: We made Zoom more engaging through computer vision, retro graphics, sentiment tracking, and data analytics.

**Built by**: Nilai Vemula, Carly Bernstein, Jack Walton, Shiv Patel

## Awards
:trophy: Most creative virtual peer-to-peer collaboration engagement aid (Alliance Bernstein)

:trophy: Best Use of Google Cloud: COVID-19 Hackathon Fund


</div>


## Demos

Devpost: https://devpost.com/software/retro-zoom

Full video demo: https://youtu.be/WGBdyyA_2VQ

Pitch video: https://youtu.be/KRNiMF1ev3Y

Scavenger hunt demo: https://youtu.be/ETCymdAjdQI

## Inspiration

Our team has been stuck on Zoom meetings for the past six months. While some of us are remote students at school this semester and others are online, we all are constantly on Zoom. The shared common experience of Zoom fatigue inspired us to brainstorm ways of making the platform better for all users. To break up the monotony of hours of virtual meetings, we decided to build a series of tools to make Zoom more engaging and track user behavior to suggest mediation strategies. For meeting hosts, we also solve the problem of not being able to accurately read the room by providing these users with a real-time graph monitoring the overall emotional state of their up to 49 attendees. 

## What it does

Our project, Retro Zoom, contains a series of interactive plug-ins that improve the overall Zoom experience. At the heart of our project, we monitor the user’s sentiment by analyzing their facial expressions. Using this data, we suggest activities for the user. To help fight Zoom fatigue, the user can select from a few of retro-themed games: Coin Grab, Scavenger Hunt, and Asteroid Dodge. At the end of their Zoom meeting, the user can generate a report of their data throughout the meeting to monitor their emotional wellbeing. For corporate or educational users, we feature group sentiment analysis for Zoom calls, where administrators can monitor the overall sentiment of their meeting attendees. This data will empower meeting hosts to calibrate their behavior to their audience in real-time. The application also empowers Zoom students to understand their own sentiment during the call by growing a mario-style pipe when the user is joyous and shrinking the pipe when the user is angry.

## How I built it

To analyze the user’s emotions as well as implement our retro-themed games, we first capture the user’s video feed using OpenCV. Once we have video frames from the webcam, our program uses computer vision tools to detect faces, queries the Google Cloud Vision API to track user sentiment, and simulates interactive games using OpenCV, PIL, and the object localization features in the Google Cloud Vision API. Finally, our modified webcam view is streamed through to a virtual camera that can interface with Zoom or any other video conferencing application.

Our user-generated reports are created by accessing data that is optionally stored in a JSON file throughout the meeting. We implement our data visualizations in Plotly and present them in a Dash dashboard with custom HTML/CSS styling.

Our group sentiment tracker was built by automating the collection of screenshots of Zoom’s gallery view. These screenshots are streamed to the Google Cloud Vision API for sentiment analysis. Using this data, we create a visualization in real-time that is shown to the user with a TKinter GUI and matplotlib.



### Technical Specs
- Python 3.7+
- [`pyvirtualcam` library](https://github.com/letmaik/pyvirtualcam) for sending our video stream to Zoom
- [`pynput` library](https://github.com/moses-palmer/pynput) for capturing user input through keystrokes
- OpenCV
- multi-threading
- Google Cloud Vision API
  - emotion analysis
  - object detection
- plotly and dash for data analysis reports
- matplotlib and tkinter for the group sentiment analysis



## Challenges I ran into

Our biggest issue was latency. When grabbing frames from the camera, the program seemed to grab 1-to-2 second old frames rather than the most recent frame. We tried a thread-based solution that continuously cleared the frame buffer, but that did not noticeably improve performance. 

We also struggled with framerate. Our program needs to maintain a quickly updating user interface, but our API requests would cause long pauses when handled in the main thread. To fix this we implemented multi-threading by sending all of the API requests to a Python ThreadPoolExecutor to get handled. 

We also had issues getting opencv to work as none of us have worked with that library in the past. 

Our final challenge was that we had trouble recording a video and getting it uploaded at the last minute. Our struggles with video editing and uploading had us quickly through together a demo.

## Accomplishments that I'm proud of

Our team is proud of the virtual webcam implementation. We were able to successfully create an interactive app that modifies your video feed and plugs that feed directly into any app that uses the camera. We are also proud of the communication, teamwork, planning, and efficient github workflow we implemented. 

We are also proud of the overall aesthetic of the product, which was guided by the Hackathon’s retro-theme. A couple of our team members we able to exercise their pixel-art and image-editing skills.
Most importantly, we are proud of the fact that we successfully built a tool that we can use in our Zoom meetings to stimulate engagement, something we think might be really fun for the student organizations we are a part of.


## What I learned

- **Nilai**: I have used Python before, but I learned a lot about how to improve performance with multi-threading. I also gained experience working in a team on a git repository through solving merge conflicts in pull requests and keeping track of different branches. I also made by first GUI in Python!
- **Jack**: I learned how to make requests to Google’s Vision APIs. 
- **Carly**: I learned how to program in Python as well as how to collaborate in group situations.
- **Shiv**: The biggest thing I learned this weekend was how to create interactive data visualizations and the importance of data cleansing.


## What's next for Retro Zoom

The performance of Retro Zoom could be further improved. Our current bottleneck is reading frames from the real camera on the device. The UI/UX could also use some touching up with more helpful instructions on how to navigate the app. Finally, we would like to extend our product to MacOS and Linux, as our current demo only works in Windows.

As a product, we believe Retro Zoom has potential business value. Some potential customers would include schools and corporations hoping to increase Zoom engagement during prolonged work-from-home periods. Teachers or managers can monitor student's attention/sentiment during classes or meetings and have live updates. These users can use this data to gauge their audience’s emotions calibrate their presentation-style in real-time to be more engaging. For more casual users, we propose a freemium model where users can take breaks during their Zoom meetings to play a short game or groups of friends play games together and compete. This business model would draw in customers through free games and data analytics, and we would provide a premium plan that could unlock more games and deeper insights into the user’s emotional wellbeing during their Zoom meetings. 





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

## Getting Started:

First, install the following dependencies (you will need Python 3.8):

- [OBS Studio](https://obsproject.com/download)
- [OBS Studio Virtual Camera Plug-in](https://obsproject.com/forum/resources/obs-virtualcam.949/)
- [Python Libraries](requirements.txt) - These can be installed by running `pip install -r requirements.txt` in the
 command line
    - [`pyvirtualcam` python library](https://github.com/letmaik/pyvirtualcam)
    - numpy
    - open cv 
    - Pillow
    - plotly
    - pandas
    - google cloud vision
    - pynput

Instructions:
1. Set up a virtual camera in OBS Studio
2. Close OBS Studio
3. Run the Python code (`python control.py` in the command line)
4. Start a Zoom meeting
5. Select OBS as your camera
6. You should see yourself, distorted and with a delay...
