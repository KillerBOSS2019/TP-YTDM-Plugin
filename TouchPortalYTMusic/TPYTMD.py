import base64
import json
import os
import threading
from time import sleep, strftime
import TouchPortalAPI
import urllib3
from TouchPortalAPI import TYPES
import requests
from sys import exit

YTMD_server = "localhost"
LoginPass = None
isBeta = False
lyricsRange = [-5, 5]
lyricsStatesList = []
statesData = ""
http = urllib3.PoolManager(num_pools=10)
isYTMDRunning = False
running = False

def createDebug():
    if os.path.isfile("./log.txt"):
        os.remove("log.txt")
        
    print('log file has been created')
    Logfile = open('log.txt', 'w')
    currenttime = (strftime('[%I:%M:%S:%p] '))
    Logfile.write("log file created At: "+currenttime)
    Logfile.write('\n')
    Logfile.write('--------------------------------------------\n')
    Logfile.close()
def writeServerData(Serverinfo):
    currenttime = (strftime('[%I:%M:%S:%p] '))
    logfile = open('log.txt', 'a')
    logfile.write(currenttime + "%s" % (Serverinfo))
    logfile.write('\n')
    logfile.close()

def YTMD_Actions(command,value=None, showdata=True):
    data = {'command':command, 'value': value}
    encoded_data = json.dumps(data).encode('utf-8')
    status = http.request('POST', f'http://{YTMD_server}:9863/query',headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
    if showdata:
        print(f'Running Command: {command} Value: {value} Status Code: {status.status}')
        writeServerData(f'Running Command: {command} Value: {value} Status Code: {status.status}')

TPClient = TouchPortalAPI.Client("YoutubeMusic")

oldPlaylist = []
oldMusicTitle = (None, -1)
lyricsClock = 0
totalTimewait = 0
HiddenLyrics = False
globalVol = 0
connectionStatus = False
def stateUpdate():
    global oldPlaylist, isYTMDRunning, Timer, oldMusicTitle, HiddenLyrics
    global lyricsClock, totalTimewait, connectionStatus
    while running:
        try:
            statesData = json.loads(http.request("GET", f"http://{YTMD_server}:9863/query", headers={"Authorization": f"bearer {LoginPass}"}).data.decode("utf-8"))
            currentPlaylist = json.loads(http.request("GET", f"http://{YTMD_server}:9863/query/playlist", headers={"Authorization": f"bearer {LoginPass}"}).data.decode("utf-8"))['list']
            queryQueue = json.loads(http.request("GET", f"http://{YTMD_server}:9863/query/queue", headers={"Authorization": f"bearer {LoginPass}"}).data.decode("utf-8"))
            Lyricsdata = json.loads(http.request("GET", f"http://{YTMD_server}:9863/query/lyrics", headers={"Authorization": f"bearer {LoginPass}"}).data.decode("utf-8"))
            isYTMDRunning = True
            if connectionStatus != isYTMDRunning:
                print("Connected to YTMD")
                connectionStatus = isYTMDRunning
        except Exception as e:
            if "refused" in str(e).split():
                isYTMDRunning = False
            else:
                isYTMDRunning = False
            if connectionStatus != isYTMDRunning:
                print("YTMD Server shutdown")
                connectionStatus = isYTMDRunning
            TPClient.settingUpdate("Status", "YTMD is Not open")
        if isYTMDRunning:
            TPClient.settingUpdate("status", "YTMD is Open")
            TPClient.stateUpdate("KillerBOSS.TouchPortal.Plugin.YTMD.States.TrackCurrentLyrics", Lyricsdata["data"])
            if oldPlaylist != currentPlaylist:
                print("Updating playlist")
                oldPlaylist = currentPlaylist
                TPClient.choiceUpdate("KillerBOSS.TouchPortal.Plugin.YTMD.Action.AddToPlaylist.Value", oldPlaylist)
                TPClient.choiceUpdate("KillerBOSS.TouchPortal.Plugin.YTMD.Action.StartPlaylist.playlistName", oldPlaylist)

            if statesData['track']['title'] != oldMusicTitle[0] or oldMusicTitle[1] != queryQueue['currentIndex']:
                oldMusicTitle = (statesData['track']['title'], queryQueue['currentIndex']);
                #print(oldMusicTitle, statesData['track']['title'])
                if statesData['track']['cover']:
                    TPClient.stateUpdate("KillerBOSS.TouchPortal.Plugin.YTMD.States.Playercover", base64.b64encode(requests.get(statesData['track']['cover']).content).decode('utf-8'))
                if isBeta:
                    YTMD_Actions("show-lyrics-hidden", showdata=False)
                    HiddenLyrics = True
                lyricsClock = 0
                totalTimewait = 0
            def get5Line(Lyrics, currentindex):
                lyrics = []
                def line(line, x):
                    try:
                        if x >= 0:
                            lyrics.append(Lyrics[x])
                        else:
                            lyrics.append(" ")
                    except (KeyError, IndexError):
                        lyrics.append(" ")
                
                for lyricsIndex in range(int(lyricsRange[0]), int(lyricsRange[1])):
                    line(Lyrics, currentindex+lyricsIndex)
                return lyrics

            def updateLyrics(index):
                lyrics = get5Line(Lyricsdata['data'].split("\n"), index)
                for lyricsState, lyric in zip(lyricsStatesList, lyrics):
                    TPClient.stateUpdate(lyricsState, lyric)
            timeBetween =  statesData['track']['duration']/len(Lyricsdata['data'].split("\n"))

            if timeBetween > 0.23:
                if not statesData['player']['isPaused'] and not statesData['track']['isAdvertisement'] and Lyricsdata['hasLoaded']:
                    totalTimewait += 0.23
                    if totalTimewait >= timeBetween:
                        lyricsClock += 1
                        totalTimewait = 0
                        updateLyrics(lyricsClock)
            try:
                TPClient.stateUpdateMany(
                    [
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PreviousSong.title",
                            "value": str(queryQueue['list'][queryQueue['currentIndex']-1]['title'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PreviousSong.author",
                            "value": str(queryQueue['list'][queryQueue['currentIndex']-1]['author'])
                        }
                    ]
                )
            except:
                pass
            try:
                if queryQueue['currentIndex']+1 < len(queryQueue['list'])-1:
                    TPClient.stateUpdateMany(
                        [
                            {
                                "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Next.title",
                                "value": str(queryQueue['list'][queryQueue['currentIndex']+1]['title'])
                            },
                            {
                                "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Next.author",
                                "value": str(queryQueue['list'][queryQueue['currentIndex']+1]['author'])
                            }
                        ]
                    )
                else:
                    TPClient.stateUpdateMany(
                        [
                            {
                                "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Next.title",
                                "value": "Unknown"
                            },
                            {
                                "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Next.title",
                                "value": "Unknown"
                            }
                        ]
                    )
            except:
                pass
            try:
                TPClient.stateUpdateMany(
                    [
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerTitle",
                            "value": str(statesData['track']['title'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Trackauthor",
                            "value": str(statesData['track']['author'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Trackalbum",
                            "value": str(statesData['track']['album'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerhasSong",
                            "value": str(statesData['player']['hasSong'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerisPaused",
                            "value": str(statesData['player']['isPaused'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerVPercent",
                            "value": str(statesData['player']['volumePercent'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Trackdurationhuman",
                            "value": str(statesData['track']['durationHuman'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Trackcurrentdurationhuman",
                            "value": str(statesData['player']['seekbarCurrentPositionHuman'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerCurrentSonglikeState",
                            "value": str(statesData['player']['likeStatus'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.isAdvertisement",
                            "value": str(statesData['track']['isAdvertisement'])
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.SeekBarStatus",
                            "value": str(round(statePercent*100)) if isinstance((statePercent := statesData['player']['statePercent']), float) else 0
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.Inlibrary",
                            "value": statesData['track']['inLibrary']
                        },
                        {
                            "id": "KillerBOSS.TouchPortal.Plugin.YTMD.States.repeatType",
                            "value": statesData['player']['repeatType']
                        }
                    ])
                TPClient.connectorUpdate("KillerBOSS.TP.Plugins.YTMD.connectors.APPcontrol", TPClient.currentStates['KillerBOSS.TouchPortal.Plugin.YTMD.States.PlayerVPercent'])
            except:
                pass
        sleep(0.23)

@TPClient.on(TYPES.onConnect)
def onConnect(data):
    global YTMD_server, LoginPass, isBeta, lyricsRange, lyricsStatesList
    global running
    print(data)
    createDebug()
    running = True
    
    YTMD_server = data['settings'][0]['IPv4 address']
    LoginPass = data['settings'][1]['Passcode']
    if data['settings'][2]["beta"] == "True":
        print("Beta is enabled")
        isBeta = True

    lyricsRange = data['settings'][3]['Lyrics Range']
    lyricsRange = lyricsRange.split(",")
        #print(lyricsRange)
    print(list(range(int(lyricsRange[0]), int(lyricsRange[1]))))
    for x in range(int(lyricsRange[0]), int(lyricsRange[1])):
        TPClient.createState("KillerBOSS.TP.Plugin.YTMD.States.ScrollLyrics.Line"+str(x), "Scrolling Lyrics Show line "+str(x), "", "Lyrics line")
        lyricsStatesList.append("KillerBOSS.TP.Plugin.YTMD.States.ScrollLyrics.Line"+str(x))
    print("Trying to Connect to", YTMD_server+":9863/query", "With passcode:", LoginPass)
    threading.Thread(target=stateUpdate).start()

@TPClient.on(TYPES.onAction)
def Actions(data):
    if isYTMDRunning:
        ActionData = json.loads(http.request("GET", f"http://{YTMD_server}:9863/query", headers={'Authorization': f'bearer {LoginPass}'}).data.decode('utf-8'))
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.Play/Pause":
            PauseStates = ActionData['player']['isPaused']
            if data['data'][0]['value'] == "Play":
                if PauseStates:
                    YTMD_Actions("track-play")
            elif data['data'][0]['value'] == "Pause":
                if PauseStates == False:
                    YTMD_Actions("track-pause")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.Next/Previous":
            if data['data'][0]['value'] == "Next":
                YTMD_Actions("track-next")
            elif data['data'][0]['value'] == "Previous":
                YTMD_Actions("track-previous")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.Like/Dislike":
            if data['data'][0]['value'] == "Like":
                YTMD_Actions("track-thumbs-up")
            elif data['data'][0]['value'] == "Dislike":
                YTMD_Actions("track-thumbs-down")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.VUp/VDown":
            if data['data'][0]['value'] == "Up":
                YTMD_Actions("player-volume-up")
            elif data['data'][0]['value'] == "Down":
                YTMD_Actions("player-volume-down")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.forward/rewind":
            if data['data'][0]['value'] == "Forward":
                YTMD_Actions("player-forward")
            elif data['data'][0]['value'] == "Rewind":
                YTMD_Actions("player-rewind")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.RepeatPic":
            repeatState = ActionData['player']['repeatType']
            if data['data'][0]['value'] == "ONE":
                if repeatState != "ONE":
                    if repeatState == "ALL":
                        YTMD_Actions("player-repeat", value="ONE")
                    elif repeatState == "NONE":
                        for x in range(2):
                            YTMD_Actions("player-repeat", value="ONE")
            elif data['data'][0]['value'] == "All":
                if repeatState != "ALL":
                    if repeatState == "ONE":
                        for x in range(2):
                            YTMD_Actions("player-repeat", value="ALL")
                    elif repeatState == "NONE":
                        YTMD_Actions("player-repeat", value="ALL")
            elif data['data'][0]['value'] == "OFF":
                if repeatState != "NONE":
                    if repeatState == "ONE":
                        YTMD_Actions("player-repeat", value="NONE")
                    elif repeatState == "ALL":
                        for x in range(2):
                            YTMD_Actions("player-repeat", value="NONE")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.mute/unmute":
            global globalVol
            if data['data'][0]['value'] == "Mute":
                globalVol = ActionData['player']['volumePercent']
                YTMD_Actions("player-set-volume", value=0)
            elif data['data'][0]['value'] == "Unmute":
                YTMD_Actions("player-set-volume", value=globalVol)
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.AddToPlaylist":
            YTMD_Actions("player-add-playlist", value=str(json.loads(http.request("GET", f"http://{YTMD_server}:9863/query/playlist", headers={"Authorization": f"bearer {LoginPass}"}).data.decode("utf-8"))['list'].index(data['data'][0]['value'])))
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.SetSeekBar":
            YTMD_Actions("player-set-seekbar", value=data['data'][0]['value'])
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.SetVolume":
            YTMD_Actions("player-set-volume", value=data['data'][0]['value'])
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.PlayTrackNumber":
            YTMD_Actions("player-set-queue", value=data['data'][0]['value'])
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.AddToLibrary":
            YTMD_Actions("player-add-library")
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.Shuffle":
            YTMD_Actions("player-shuffle")    

        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.StartPlaylist":
            YTMD_Actions("start-playlist", data['data'][0]['value'])
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.PlayURL":
            YTMD_Actions("play-url", data['data'][0]['value'])
        if data['actionId'] == "KillerBOSS.TouchPortal.Plugin.YTMD.Action.SkiAd":
            YTMD_Actions("skip-ad")

@TPClient.on(TYPES.onConnectorChange)
def connectorManager(data):
    if data['connectorId'] == "KillerBOSS.TP.Plugins.YTMD.connectors.APPcontrol" and isYTMDRunning:
        YTMD_Actions("player-set-volume", data['value'])

@TPClient.on(TYPES.onShutdown)
def Disconnect(data): 
    global running
    running = False
    try:
        TPClient.disconnect()
    except (ConnectionResetError,AttributeError):
        pass
    print("Shutting Down")
    exit(0)


TPClient.connect()
