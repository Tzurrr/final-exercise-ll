import os
import sys
import time
from threading import Thread
import time
import datetime
import redis
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer
from queue import Queue
from threading import Thread
import os
from watchdog.events import FileCreatedEvent, FileClosedEvent
import remove_older
import sender
import verifier
import dot_finder
import elogger
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed


dir_path = "/home/tzur/all-the-photos"

def process_queue(q):
    counter = 0
    half_two_arr = []
    half_one_arr = []
    while True:
        counter += 1
        half_one_arr = remove_older.remove(half_one_arr)
        half_two_arr = remove_older.remove(half_two_arr)
        if not q.empty():
            event = q.get()
            dot = dot_finder.find(event.src_path)
            elogger.write("arrivedtoserver")

            if event.src_path[:dot][-1] != "a" and event.src_path[:dot][-1] != "b":
               # print("irrelevant")
                os.remove(event.src_path)

            elif event.src_path[:dot][-1] == "a":
                #print("first half")
                r.set(f"{event.src_path[:dot - 2]}", event.src_path)
                half_one_arr.append((event.src_path, datetime.datetime.utcnow()))
#                if len(half_one_arr) > 0:
 #                   is_valid = verifier.verify(half_one_arr, half_two_arr)
  #                  if is_valid:
   #                     sender.send(event.src_path, half_two_arr)

            elif event.src_path[:dot][-1] == "b":
                #print("second half")
                half_two_arr.append((event.src_path, datetime.datetime.utcnow()))
                if len(half_one_arr) > 0:
                    is_valid = verifier.verify(half_one_arr, half_two_arr)
                    if is_valid:
                        sender.send(event.src_path)


class FileWatchdog(PatternMatchingEventHandler):
    def __init__(self, queue, patterns):
        PatternMatchingEventHandler.__init__(self, patterns=["*"], ignore_patterns=None, ignore_directories=False, case_sensitive=True)
        self.queue = queue

    def process(self, event):
        self.queue.put(event)
#        print(("a", event.event_type))

    def on_closed(self, event):
        self.process(event)

if __name__ == "__main__":
    r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
    watchdog_queue = Queue()

    for file in os.listdir(dir_path):
        filename = os.path.join(dir_path, file)
        event = FileClosedEvent(filename)
        watchdog_queue.put(event)
        
    #with ProcessPoolExecutor() as executor:
      #  a = executor.submit(process_queue(watchdog_queue), watchdog_queue)
       # a.result()

    event_handler = FileWatchdog(watchdog_queue, patterns="*.ini")
    observer = Observer()
    observer.schedule(event_handler, path=dir_path)
    observer.start()
    try:
   #     while (True):
        with ProcessPoolExecutor() as executor:
            a = executor.submit(process_queue(watchdog_queue), watchdog_queue)
            a.result()

    #        time.sleep(10)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


