import socket, requests, json, os.path, threading, sys, base64, os
from time import time
from time import sleep
import urllib3, sys

'''
I changed From using Requests library to urllib3 library 
'''


# TP socket information
TPHOST = '127.0.0.1'
TPPORT = 12136

# creating socket connection with Touch Portal
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TPHOST, TPPORT))
except:
    print('Cannot connect to the server')
s.sendall(b'{"type":"pair","id":"YoutubeMusic"}\n')
data = s.recv(1024)
print(repr(data))
running = True
http = urllib3.PoolManager(num_pools=100)
global LoginPass
LoginPass = json.loads(data)['settings'][0]['Passcode']
print(LoginPass)


#This Function is used for Checking if YTMD is open or Web Server is open or not If not UpdateStates will not run until YTMD is open
def MainData():
    global FMainData, Trackinfo, Lyricsinfo, Http_Status, running
    FMainData = threading.Timer(0.2,MainData)
    FMainData.start()
    if running:
        start = int(time() * 1000)
        try:
            Trackinfo = http.request('GET', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass})
            Lyricsinfo = http.request('GET', 'http://localhost:9863/query/lyrics', headers={'Authorization': 'bearer %s' % LoginPass})
            Trackinfo = Trackinfo.data.decode('utf-8')
            Trackinfo = json.loads(Trackinfo)
            Lyricsinfo = Lyricsinfo.data.decode('utf-8')
            Lyricsinfo = json.loads(Lyricsinfo)
            s.sendall(('{"type":"settingUpdate", "name":"status", "value":"YTMD is open"}\n').encode())
            Http_Status = True
        except:
            Http_Status = False
            s.sendall(('{"type":"settingUpdate", "name":"status", "value":"YTMD is Not Open"}\n').encode())
        end = int(time() * 1000)
    else:
        FMainData.cancel()

OG_Track = 0
#This Function is for sending datas to the TouchPortal Server If MainData() checks YTMD is not open this function will not run    
def updateStates():
    global OG_Track
    timer = threading.Timer(0.22,updateStates)
    timer.start()
    #print('Http_Status: '+str(Http_Status))
    if running:
        if Http_Status:
            start = int(time() * 1000)
            try:
                Tracktitle = Trackinfo['track']['title'] #done
                s.sendall(('{"type":"stateUpdate", "id":"PlayerTitle", "value":"%s"}\n' % Tracktitle).encode())
            except Exception as e:
                print(str(e)+' 1')
                pass
            try:
                if Trackinfo['track']['cover'] != OG_Track:
                    OG_Track = Trackinfo['track']['cover']
                    print("updating Image")
                    Trackcover = Trackinfo['track']['cover'] #done
                    Trackcover = requests.get(Trackcover).content
                    Trackcover = base64.b64encode(Trackcover)
                    s.sendall(('{"type":"stateUpdate", "id":"Playercover", "value":"%s"}\n' % Trackcover.decode("ascii")).encode())
            except Exception as e:
                print(str(e)+' 2')
            try:
                Trackauthor = Trackinfo['track']['author'] #done
                s.sendall(('{"type":"stateUpdate", "id":"Trackauthor", "value":"%s"}\n' % Trackauthor).encode())
            except Exception as e:
                print(str(e)+' Error')
            try:
                Trackalbum = Trackinfo['track']['album'] #done
                s.sendall(('{"type":"stateUpdate", "id":"Trackalbum", "value":"%s"}\n' % Trackalbum).encode())
            except Exception as e:
                print(str(e)+' 4')
            try:
                PlayerhasSong = Trackinfo['player']['hasSong'] #done
                s.sendall(('{"type":"stateUpdate", "id":"PlayerhasSong", "value":"%s"}\n' % PlayerhasSong).encode())
            except Exception as e:
                print(str(e)+' 5')
            try:
                PlayerisPaused = Trackinfo['player']['isPaused']#done
                if PlayerisPaused == True:
                    PlayerisPaused = 'Paused'
                else:
                    PlayerisPaused = 'Playing'
                s.sendall(('{"type":"stateUpdate", "id":"PlayerisPaused", "value":"%s"}\n' % PlayerisPaused).encode())
            except Exception as e:
                print(str(e)+' Error PlayerisPaused')
            try:
                PlayerVPercent = Trackinfo['player']['volumePercent']#done
                PlayerVPercent = str(PlayerVPercent)+'%'
                s.sendall(('{"type":"stateUpdate", "id":"PlayerVPercent", "value":"%s"}\n' % PlayerVPercent).encode())
            except Exception as e:
                print(str(e)+' 7')
            try:
                Trackdurationhuman = Trackinfo['track']['durationHuman']#done
                s.sendall(('{"type":"stateUpdate", "id":"Trackdurationhuman", "value":"%s"}\n' % Trackdurationhuman).encode())
            except Exception as e:
                print(str(e)+' Error durationHuman')
            try:
                TrackCurrentdurationhuman = Trackinfo['player']['seekbarCurrentPositionHuman']#done
                s.sendall(('{"type":"stateUpdate", "id":"Trackcurrentdurationhuman", "value":"%s"}\n' % TrackCurrentdurationhuman).encode())
            except Exception as e:
                print(str(e)+' 9')
            try:
                TrackCurrentlikeState = Trackinfo['player']['likeStatus']#done
                s.sendall(('{"type":"stateUpdate", "id":"PlayerCurrentSonglikeState", "value":"%s"}\n' % TrackCurrentlikeState).encode())
            except Exception as e:
                print(str(e)+' 10')
            try:
                TrackCurrentLyrics = Lyricsinfo['data']
                TrackCurrentLyrics = TrackCurrentLyrics.replace('\n\n', ' ')
                TrackCurrentLyrics = TrackCurrentLyrics.replace('\n', '. ')
                s.sendall(('{"type":"stateUpdate", "id":"TrackCurrentLyrics", "value":"%s"}\n' % TrackCurrentLyrics).encode())
            except Exception as e:
                print(str(e)+' 11')
            try:
                isAdvertisement = Trackinfo['track']['isAdvertisement']
                s.sendall(('{"type":"stateUpdate", "id":"isAdvertisement", "value":"%s"}\n' % isAdvertisement).encode())
            except Exception as e:
                print(str(e)+' 12')
            try:
                repeatType = Trackinfo['player']['repeatType']
                if repeatType == 'NONE':
                    repeatType = 'OFF'    
                s.sendall(('{"type":"stateUpdate", "id":"repeatType", "value":"%s"}\n' % repeatType).encode())
            except Exception as e:
                print(str(e)+' 13')
            try:
                Statusbar = Trackinfo['player']['statePercent']
                Statusbar = int(round((Statusbar*100),0))
                s.sendall(('{"type":"stateUpdate", "id":"SeekBarStatus","value":"%s"}\n' % Statusbar).encode())
            except Exception as e:
                print(str(e)+' 14')
            try:
               Inlibrary = Trackinfo['track']['inLibrary']
               s.sendall(('{"type":"stateUpdate", "id":"inLibrary","value":"%s"}\n' % Inlibrary).encode())
            except Exception as e:
                print(str(e)+' inLibrary')
            end = int(time() * 1000)
    else:
        timer.cancel()
MainData()
updateStates()


#This is the main program for Actions and if Server sends Close plugin this will change to False so this program will Exit
while running:
    CHUNK_SIZE = 4000
    buffer = bytearray()
    data = s.recv(CHUNK_SIZE)
    buffer.extend(data)
    firstline = buffer[:buffer.find(b'\n')]
    d = json.loads(firstline)
    if running == True:
        if d != None and d['type'] == 'closePlugin':
            if d['pluginId'] == 'YoutubeMusic':
                s.close()
                print('YoutubeMusic Plugin has been closed!')
                running = False
                Http_Status = False
                sys.exit()
        if d['type'] == "settings":
            LoginPass = d['values'][0]['Passcode']
        if Http_Status == True:
            if d != None and d['type'] != 'closePlugin' and running == True and d['type'] != 'listChange' and d['type'] != "broadcast" and d['type'] != "settings":
                print(d)
                if d['actionId'] == 'Play/Pause':
                    if d['data'][0]['id'] == 'PlayPause' and d['data'][0]['value'] == 'Play':
                        data = {'command':'track-play'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'PlayPause' and d['data'][0]['value'] == 'Pause':
                        data = {'command':'track-pause'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'Next/Previous':
                    if d['data'][0]['id'] == 'Next&Previous' and d['data'][0]['value'] == 'Next':
                        data = {'command':'track-next'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'Next&Previous' and d['data'][0]['value'] == 'Previous':
                        data = {'command':'track-previous'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'Like/Dislike' and d['data'][0]['id'] == 'Like&Dislike':
                    if d['data'][0]['value'] == 'Like':
                        data = {'command':'track-thumbs-up'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['value'] == 'Dislike':
                        data = {'command':'track-thumbs-down'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                        requests.post('http://localhost:9863/query', json={"command":"track-thumbs-down"},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'VUp/VDown':
                    if d['data'][0]['id'] == 'UPORDOWN' and d['data'][0]['value'] == 'Up':
                        data = {'command':'player-volume-up', 'value':str(d['data'][1]['value'])}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'UPORDOWN' and d['data'][0]['value'] == 'Down':
                        data = {'command':'player-volume-down', 'value':str(d['data'][1]['value'])}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'forward/rewind':
                    if d['data'][0]['id'] == 'ForwardANDRewind' and d['data'][0]['value'] == 'Forward':
                        data = {'command':'player-forward'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'ForwardANDRewind' and d['data'][0]['value'] == 'Rewind':
                        data = {'command':'player-rewind'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'Shuffle':
                    if d['type'] == 'action' and d['actionId'] == 'Shuffle':
                        data = {'command':'player-shuffle'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'AddtoThis':
                    if d['data'][0]['id'] == 'Library':
                        PlayList =  requests.get('http://localhost:9863/query/playlist',headers={'Authorization': 'bearer %s' % LoginPass}).text
                        PlayList = json.loads(PlayList)
                        print(PlayList)
                        PlayList = PlayList['list'].index(d['data'][0]['value'])
                        data = {'command':'player-add-playlist', 'value':str(PlayList)}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'AddLibrary' and d['type'] == 'action':
                    data = {'command':'player-add-library'}
                    encoded_data = json.dumps(data).encode('utf-8')
                    http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'PlayTrack' and d['type'] == 'action':
                    PlayTrack = int(d['data'][0]['value'])
                    PlayTrack = ((PlayTrack > 0) * (PlayTrack-1))
                    data = {'command':'player-set-queue','value':str(PlayTrack)}
                    encoded_data = json.dumps(data).encode('utf-8')
                    http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'SetSeekBar':
                    if d['data'][0]['id'] == 'SetSeek' and d['actionId'] == 'SetSeekBar':
                        data = {'command':'player-set-seekbar', 'value': str(d['data'][0]['value'])}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['data'][0]['id'] == 'RepeatPic':
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'All':
                        data = {'command':'player-repeat', 'value': 'ALL'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'ONE':
                        data = {'command':'player-repeat', 'value': 'ONE'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'OFF':
                        data = {'command':'player-repeat', 'value': 'NONE'}
                        encoded_data = json.dumps(data).encode('utf-8')
                        http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)
                if d['actionId'] == 'SetVolume' and d['data'][0]['id'] == 'SetVolume':
                    data = {'command':'player-set-volume', 'value': str(d['data'][0]['value'])}
                    encoded_data = json.dumps(data).encode('utf-8')
                    http.request('POST', 'http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}, body=encoded_data)



