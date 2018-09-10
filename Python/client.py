#! /usr/local/bin/python3
import zmq
import time
import random

from functools import partial
from random import random
from threading import Thread
import time

from bokeh.layouts import gridplot, row, layout, column
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen

ip = 'localhost'
port_sub = '1234'
TIMEOUT = 10000
# this must only be modified from a Bokeh session callback
source = ColumnDataSource(dict(time=[], x=[], y=[], z=[]))

def initialize_sub_socket(ip, port_sub):
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_string = "%s:%s" % (ip, port_sub)
    print("Connecting to %s" % socket_string)
    # you can run this multiple times to receive from multiple ports
    socket_sub.connect("tcp://%s:%s" % (ip, port_sub))
    print('Set ZMQ Subscriber with topic filter')
    return(socket_sub)

doc = curdoc()

@gen.coroutine
def update(msgData):
    print("in here")
    x, y, z = msgData.split(' ')
    cur_time = time.time()
    new_data = dict(time=[cur_time], x=[x], y=[y], z=[z])
    print("source.data: ", source.data['time'], source.data['x'],source.data['y'],source.data['z'])
    source.stream(new_data,100)

def subscribe_and_stream():
    while True:
        # do some blocking computation
        #time.sleep(0.1)
        global socket_sub, poller, source
        socket_sub.setsockopt(zmq.SUBSCRIBE, "")
        count = 0
        try:
            response = socket_sub.recv(zmq.NOBLOCK)
            topic, messagedata = response.split()
            print(messagedata)
            x, y, z = messagedata.split(' ')
            cur_time = time.time()
            new_data = dict(time=[cur_time], x=[x], y=[y], z=[z])
            print("source.data: ", source.data['time'], source.data['x'],source.data['y'],source.data['z'])
            source.stream(new_data,100)
            # doc.add_next_tick_callback(partial(update, response))
            continue
            time.sleep(0.8)

        except KeyboardInterrupt:
            print("CLEAN UP CLEAN UP EVERYBODY CLEANUP")
            while not socket_sub.closed:
                #TODO check if fn is in right place
                while not socket_sub.closed:
                    print("close the socket!")
                    socket_sub.close()
                    sys.exit(0)

fig = figure(plot_width=2000, plot_height=750)
fig.line(source=source, x='time', y='x', line_width=2, alpha=0.85, color='red')
doc.add_root(fig)

socket_sub = initialize_sub_socket(ip, port_sub)
poller = zmq.Poller()

thread = Thread(target=subscribe_and_stream)
thread.start()
