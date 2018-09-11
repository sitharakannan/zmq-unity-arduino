using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Globalization;

public class wrmhlRead : MonoBehaviour {

	wrmhl myDevice = new wrmhl(); // wrmhl is the bridge beetwen your computer and hardware.

	[Tooltip("SerialPort of your device.")]
	public string portName = "COM3";

	[Tooltip("Baudrate")]
	public int baudRate = 250000;


	[Tooltip("Timeout")]
	public int ReadTimeout = 20;

	[Tooltip("QueueLenght")]
	public int QueueLenght = 1;

    void Start () {
		myDevice.set (portName, baudRate, ReadTimeout, QueueLenght); // This method set the communication with the following vars;
		                                                            //Serial Port, Baud Rates, Read Timeout and QueueLenght.
		myDevice.connect (); // This method open the Serial communication with the vars previously given.
    }

	// Update is called once per frame
	void Update () {
        float arduinoMin = 0.0f;
        float arduinoMax = 1024.0f;
        float arduinoRange = arduinoMax - arduinoMin;
        //float transformMin = -5.0f;
        //float transformMax = 5.0f;
        //float transformRange = transformMax - transformMin;
        print (myDevice.readQueue () ); // myDevice.read() return the data coming from the device using thread.
        var n = float.Parse(myDevice.readQueue(), CultureInfo.InvariantCulture.NumberFormat);
        var modifiedN = (n - arduinoMin) / arduinoRange;
        transform.position = new Vector3(modifiedN, transform.position.y, transform.position.z);
    }

	void OnApplicationQuit() { // close the Thread and Serial Port
		myDevice.close();
	}
}
