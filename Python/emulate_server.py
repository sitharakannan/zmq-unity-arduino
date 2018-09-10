import zmq
import time
import sys
import random
port = "1234"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = random.randrange(9999,10005)
    msg = str(random.uniform(-1.0, 1.0)) + " " + str(random.uniform(-1.0, 1.0)) + " " + str(random.uniform(-1.0, 1.0))
    print(msg)
    socket.send_string("%d %s" % (topic, msg))
    time.sleep (1)
