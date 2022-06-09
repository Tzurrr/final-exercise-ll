import redis
import os
import requests
import dot_finder
import elogger
import time
import urllib

def send(filepath: str, *args):
    r = redis.Redis()
    dot = dot_finder.find(filepath)
    get_val = r.get(f"{filepath[:dot - 2]}")

  #  if get_val == filepath:
#        for i in args:
 #           print(i)
        #    if i[0][:dot] == filepath[:dot-1] +"b":
         #       get_val = i[0]

    arr = [("files", open(get_val, "rb")), ("files", open(filepath, "rb"))]
    resp = requests.post(url="http://127.0.0.1:80/", files=arr)
    if str(resp.json) == "<bound method Response.json of <Response [200]>>":
        elogger.write("sent")
        os.remove(get_val)
        os.remove(filepath)
        print(resp.json)
    else:
        elogger.write("didntsent")
        os.remove(get_val)
        os.remove(filepath)
        print(resp.json)
