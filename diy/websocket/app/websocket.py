
# coding: utf-8
import json
import time
import subprocess

def handle_websocket(ws):
    while True:
        message = ws.receive()
        if message is None:
            time.sleep(0.1)
            #break
        else:
            message = json.loads(message)
            #p = subprocess.Popen([message['output']], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
            #p.wait()



            ws.send(json.dumps({'output': message['output']}))
