# zmq-unity-arduino


On executing Arduino.ino, you can read the values of joystick on console of Unity. Ensure Serial Monitor is closed on Arduino IDE

Python contains several files.
Run "python server.py" to send values to ClientObject.cs which uses received values to move position of cube in Unity
Run "bokeh serve --show reqrep_client.py" to plot values received from ServerObject.cs from Unity
^ Can confirm works with python2, TODO: check for python3

UnityZeroMQExample contains all Assets and codes for Unity, cube object scripts

TODO: Honestly I dont know if we require Wrmhl Unity here of if all required packages are already in UnityZeroMQExample folder
