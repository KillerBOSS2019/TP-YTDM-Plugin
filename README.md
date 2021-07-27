
## TouchPortal Youtube Music Desktop Plugin
- [TouchPortal YTMD Plugin](#touchportal-youtube-musicdesktopplugin)
  - [Description](#description)
  - [Action/States/Events](#actionstatesevents)
    - [Action](#action)
    - [States](#states)
    - [Events](#events)
  - [Installation Guide](#installation)
  - [Info](#info)

## Description
This is an integration for [TouchPortal](https://www.touch-portal.com/) that Allow you to control [Youtube Music Desktop app](https://ytmdesktop.app)

## Action/States/Events
### action
  - [Action] YT Music Playback Play/Pause (Allows you to Pause/Play current Song)
  - [Action] YT Music Playback Next/Previous (let you play previous song or next song)
  - [Action] YT Music Control Like/Dislike (Allows you to Like or Dislike current playing Song)
  - [Action] YT Music Control Volume (Allows you Increase/Decrease volume Note: Values is unchangable)
  - [Action] YT Music Playback seek (Allows you to Forward/Rewind by 10 Seconds)
  - [Action] YT Music Playback Repeat (Allows you to change Repeat States to OFF/ONE/ALL)
  - [Action] YT Music add Current Track to Playlist (Allows you to add current playing song to a X playlist)
  - [Action] YT Music Set seek (Allows you to set position of the Song)
  - [Action] YT Music Set Volume (Allows you to set volume from 0 to 100%)
  - [Action] YT Music Playback Play/Pause (Allows you to Pause/Play current Song)
  - [Action] YT Music Play Track (Allows you to play X queue song)
  - [Action] YT Music Add to Library (Allows you to add current song to your library)
  - [Action] YT Music Playback Shuffle (Shuffles current Song queue)
### Events
  - [Events] YT Music is Paused (Trigger True/False if Song is paused)
  - [Events] YT Music Song like States (Trigger if Like states is INDIFFERENT/LIKE/DISLIKE)
  - [Events] YT Music is Advertisement (Trigger if current is Playing Ads True/False)
  - [Events] YT Music Song Reoeat States (Trigger if Repeat states changes to OFF/ONE/ALL)
### States
  - [States] YT Music Song Title (Show current Song title)
  - [States] YT Music Cover Art (Show current playing Song cover)
  - [States] YT Music Song Author (Show current Song Author)
  - [States] YT Music Current Album (Show current Song Album)
  - [States] YT Music PlayerhasSong (Show if player is playing Song True/False)
  - [States] YT Music Play/Pause States (Show if current song is Paused True/False)
  - [States] YT Music Current Volume (Show current Volume 0-100 in percent)
  - [States] YT Music Song Length (Show how long is the Song format 00:00)
  - etc... you get the point


![image](https://user-images.githubusercontent.com/55416314/127076685-18ca4b8e-f5db-422b-83bd-931b190bbe09.png)


![image](https://user-images.githubusercontent.com/55416314/127077219-de1dc662-1a23-4516-9f07-58ae1ae9215e.png)

## installation
- Make sure you have latest version of YTMD installed should be Version 1.13+ otherwise Download it [Youtube Music Desktop app](https://ytmdesktop.app)
- Download latest version of YTMD Plugin

![image](https://user-images.githubusercontent.com/55416314/127077530-738e46a4-b47b-4a41-89f4-06e55e4c2973.png)
- Open TouchPortal and click Import Plugin and Select the Downloaded .tpp file

![image](https://user-images.githubusercontent.com/55416314/127077644-ae29c36b-871f-4cf6-8def-f44907fe14aa.png)

- If this is your first Plugin you may need to restart TouchPortal then it warns you if you trust this Plugin and click Trust this
- Now we will need to enable Web communication in Youtube Music Desktop on main menu hit gear icon near your Youtube account icon
- and Goto Integrations and Enable `Remote control`

![image](https://user-images.githubusercontent.com/55416314/127077944-2b6d8191-1bcb-42cf-a98b-0e4482dcece3.png)
- and Then let's head over to TouchPortal Settings. Type the password from YTMD from `Protect remote control with password` should be in blue color into Passcode entry in the TouchPortal settings

![image](https://user-images.githubusercontent.com/55416314/127078060-a5d97850-fd19-42cd-b0ae-24f8c833bf56.png)
