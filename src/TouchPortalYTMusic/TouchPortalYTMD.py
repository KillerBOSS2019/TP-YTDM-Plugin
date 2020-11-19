import socket, requests, json, os.path, threading, sys, base64, os
from time import time
from time import sleep

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
Plugin_close = b'{"pluginId":"YoutubeMusic","type":"closePlugin"}\r\n' # not in use
path = os.getcwd()
filepath = os.path.join(path,"Login.json")
if not os.path.isfile("Login.json"):
    print("Could not find Login.json file Creating and restore to default")
    LoginData = {}
    LoginData['Password']= 'XXXXX'
    with open("Login.json","w") as Config:
        json.dump(LoginData,Config)
        Config.close()
this_dir = os.path.dirname(os.path.abspath(__file__))
LoginPass = open(os.path.join(this_dir, 'Login.json'))
LoginPass = json.load(LoginPass)
LoginPass = LoginPass['Password']
print(LoginPass)
Http_Status = True
def MainData():
    global FMainData
    if running:
        FMainData = threading.Timer(0.4,MainData)
        FMainData.start()
    else:
        quit()
    start = int(time() * 1000)
    global Trackinfo, Lyricsinfo
    def TrackinfoRequests():
        global Trackinfo
        try:
            Trackinfo = requests.get('http://localhost:9863/query', headers={'Authorization': 'bearer %s' % LoginPass}).json()
            Http_Status = True
        except:
            Http_Status = False
            print('waiting for YTMD')
    def LyricsinfoRequests():
        global Lyricsinfo
        try:
            Lyricsinfo = requests.get('http://localhost:9863/query/lyrics', headers={'Authorization': 'bearer %s' % LoginPass}).json()
            Http_Status = True
        except:
            Http_Status = False
            print('waiting for YTMD')
    TrackinfoData = threading.Thread(target=TrackinfoRequests)
    LyricsData = threading.Thread(target=LyricsinfoRequests)
    TrackinfoData.start()
    LyricsData.start()
    TrackinfoData.join()
    LyricsData.join()
    end = int(time() * 1000)
    print(f"MainData() took {end-start}ms")
    
def updateStates():
    timer = threading.Timer(0.2,updateStates)
    timer.start()
    print('Http_Status: '+str(Http_Status))
    if running:
        start = int(time() * 1000)
        if Http_Status:
            try:
                Tracktitle = Trackinfo['track']['title'] #done
                s.sendall(('{"type":"stateUpdate", "id":"PlayerTitle", "value":"%s"}\n' % Tracktitle).encode())
            except Exception as e:
                print(str(e)+' 1')
                pass
            try:
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
                print(str(e)+' 3 Error')
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
                print(Statusbar)
            except Exception as e:
                print(str(e)+' 14')
            try:
               Inlibrary = Trackinfo['track']['inLibrary']
               s.sendall(('{"type":"stateUpdate", "id":"inLibrary","value":"%s"}\n' % Inlibrary).encode())
            except Exception as e:
                print(str(e)+' 15')
            end = int(time() * 1000)
            print(f"UpdateStatus() took {end-start}ms")
    else:
        timer.cancel()
MainData()
updateStates()



while running:
    print('test')
    CHUNK_SIZE = 4000
    buffer = bytearray()
    data = s.recv(CHUNK_SIZE)
    buffer.extend(data)
    if b'\n' in data or not data:
        pass
    firstline = buffer[:buffer.find(b'\n')]
    print(firstline)
    d = firstline
    d = json.loads(d)
    if running == True:
        if d['type'] == 'closePlugin':
            if d['pluginId'] == 'YoutubeMusic':
                s.close
                print('YoutubeMusic Plugin has been closed!')
                running = False
                Http_Status = False
        if Http_Status:
            if d['type'] != 'closePlugin' and running == True and d['type'] != 'listChange':
                if d['actionId'] == 'Play/Pause':
                    if d['data'][0]['id'] == 'PlayPause' and d['data'][0]['value'] == 'Play':
                        requests.post('http://localhost:9863/query', json={'command':'track-play'},headers={'Authorization': 'bearer %s' % LoginPass}).text
                    if d['data'][0]['id'] == 'PlayPause' and d['data'][0]['value'] == 'Pause':
                        requests.post('http://localhost:9863/query', json={'command':'track-pause'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'Next/Previous':
                    if d['data'][0]['id'] == 'Next&Previous' and d['data'][0]['value'] == 'Next':
                        requests.post('http://localhost:9863/query', json={'command':'track-next'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['id'] == 'Next&Previous' and d['data'][0]['value'] == 'Previous':
                        requests.post('http://localhost:9863/query', json={'command':'track-previous'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'Like/Dislike' and d['data'][0]['id'] == 'Like&Dislike':
                    print('running like action')
                    if d['data'][0]['value'] == 'Like':
                        requests.post('http://localhost:9863/query', json={'command':'track-thumbs-up'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['value'] == 'Dislike':
                        requests.post('http://localhost:9863/query', json={"command":"track-thumbs-down"},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'VUp/VDown':
                    if d['data'][0]['id'] == 'UPORDOWN' and d['data'][0]['value'] == 'Up':
                        requests.post('http://localhost:9863/query', json={'command':'player-volume-up'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['id'] == 'UPORDOWN' and d['data'][0]['value'] == 'Down':
                        requests.post('http://localhost:9863/query', json={'command':'player-volume-down','value':str(d['data'][1]['value'])},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'forward/rewind':
                    if d['data'][0]['id'] == 'ForwardANDRewind' and d['data'][0]['value'] == 'Forward':
                        requests.post('http://localhost:9863/query', json={'command':'player-forward'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['id'] == 'ForwardANDRewind' and d['data'][0]['value'] == 'Rewind':
                        requests.post('http://localhost:9863/query', json={'command':'player-rewind'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'Shuffle':
                    if d['type'] == 'action' and d['actionId'] == 'Shuffle':
                        requests.post('http://localhost:9863/query', json={'command':'player-shuffle'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'AddtoThis':
                    if d['data'][0]['id'] == 'Library':
                        PlayList =  requests.get('http://localhost:9863/query/playlist',headers={'Authorization': 'bearer %s' % LoginPass}).text
                        PlayList = json.loads(PlayList)
                        print(PlayList)
                        PlayList = PlayList['list'].index(d['data'][0]['value'])
                        requests.post('http://localhost:9863/query', json={'command':'player-add-playlist','value':str(PlayList)},headers={'Authorization': 'bearer %s'%LoginPass})
                if d['actionId'] == 'AddLibrary' and d['type'] == 'action':
                    requests.post('http://localhost:9863/query', json={'command':'player-add-library'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'PlayTrack' and d['type'] == 'action':
                    PlayTrack = int(d['data'][0]['value'])
                    PlayTrack = ((PlayTrack > 0) * (PlayTrack-1))
                    requests.post('http://localhost:9863/query', json={'command':'player-set-queue','value':str(PlayTrack)},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['actionId'] == 'SetSeekBar':
                    if d['data'][0]['id'] == 'SetSeek' and d['actionId'] == 'SetSeekBar':
                        requests.post('http://localhost:9863/query', json={'command':'player-set-seekbar', 'value': str(d['data'][0]['value'])},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['data'] == 'RepeatPic':
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'All':
                        requests.post('http://localhost:9863/query', json={'command':'player-repeat', 'value': 'ALL'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'ONE':
                        requests.post('http://localhost:9863/query', json={'command':'player-repeat', 'value': 'ONE'},headers={'Authorization': 'bearer %s' % LoginPass})
                    if d['data'][0]['id'] == 'RepeatPic' and d['actionId'] == 'Repeat' and d['data'][0]['value'] == 'OFF':
                        requests.post('http://localhost:9863/query', json={'command':'player-repeat', 'value': 'NONE'},headers={'Authorization': 'bearer %s' % LoginPass})
                if d['data'][0]['id'] == 'SetVolume' and d['actionId'] == 'SetVolume':
                    print('Setting Volume')
                    requests.post('http://localhost:9863/query', json={'command':'player-set-volume', 'value': str(d['data'][0]['value'])},headers={'Authorization': 'bearer %s' % LoginPass})



