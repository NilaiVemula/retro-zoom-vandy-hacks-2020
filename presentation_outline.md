**Format**: 90-sec video, record on OBS Studio

# Problem Statement (30 sec)
- powerpoint (1 or 2 slides)
- Zoom fatigue
- interactivity

- im in a long zoom meeting, i look bored, teacher notices everyone is bored based on her analytics, and decided to initiate <retro-zoom> for the group. 

# Demo
- recording on OBS Studio - or whatever's fastest - Shiv's fast computer
- I see the popup, edited cut footage of a few seconds of each of our games
- teacher sees positive reflection in the analytics at the end

- explain some technical stuff? How the program works 
- can we put screenshots in the write-up? Yes, link to images in md

- face detection and sentiment tracker (emotion report)
- interactive games (retro style)
- pop-up (timer)

- group sentiment tracker for classrooms
    - 15 sec demo with group zoom call and bar graphs
    


# Write-up

## Inspiration

problem statements

## What it does

breakdown of features

## How I built it

### Technical Specs
- Python
- virtual camera
- OpenCV
- multi-threading
- google api
  - emotion analysis
  - object detection
- plotly and dash for data analysis reports
- matplotlib and tkinter for the classroom group sentiment



## Challenges I ran into
- dropping frames -> multithreading to speed up API requests
- image processing with opencv

## Accomplishments that I'm proud of

- virtual webcam
- pixel art
- making my first GUI in Python

## What I learned
- learned python

## What's next for Retro Zoom

### Future Ideas
- improve performance
- make a more friendly UI

### Business Model
- teachers can monitor student's attention/sentiment during class
- businesses can monitor productivity
- sell to students to teachers or sell to students
  - teachers: monitor emotional wellbeing of their students
  - students: productivity, keep track of their own emotional health during class
- freemium for indivduals
  - play games with your friends
  - upgrade to unlock more games, get emotional reports, in-app purchases for free coins
