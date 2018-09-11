import zmq
import sys

from functools import partial
from random import random
from threading import Thread
import time

from bokeh.layouts import gridplot, row, layout, column
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure

from tornado import gen

port = "12346"
TIMEOUT = 10000
# this must only be modified from a Bokeh session callback
source = ColumnDataSource(dict(time=[], x=[], y=[], z=[]))

context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)


doc = curdoc()

@gen.coroutine
def update(msgData):
    print("in here")
    x, y, z = msgData.split(' ')
    x = float(x)
    y = float(y)
    z = float(z)
    print x, type(x), y, type(y), z, type(z)
    cur_time = time.time()
    new_data = dict(time=[cur_time], x=[x], y=[y], z=[z])
    #print("source.data: ", source.data['time'], source.data['x'],source.data['y'],source.data['z'])
    source.stream(new_data,100)

def subscribe_and_stream():
    try:
        while True:
            print "Sending request "
            socket.send ("request")
            #  Get the reply.
            message = socket.recv()
            print "Received reply: ", message
            doc.add_next_tick_callback(partial(update, message))
    except KeyboardInterrupt:
        while not socket_sub.closed:
            print("close the socket!")
            socket_sub.close()
            sys.exit(0)


fig = figure(plot_width=1000, plot_height=750)
fig.line(source=source, x='time', y='x', line_width=2, alpha=0.85, color='red')
fig.line(source=source, x='time', y='y', line_width=4, alpha=0.5, color='green')
fig.line(source=source, x='time', y='z', line_width=2, alpha=0.85, color='blue')
doc.add_root(fig)

thread = Thread(target=subscribe_and_stream)
thread.start()
