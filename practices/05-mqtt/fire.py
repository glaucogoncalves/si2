import threading
import random as rnd
import paho.mqtt.client as mqtt
import sys

class Room():

    client = None
    name = None
    fire = False
    temp = None
    smoke = None
    sprinkler = False

    thF = None #Thread for controlling Fire
    thT = None #Thread for controlling Temperature Sensor
    thS = None #Thread for controlling Smoke Sensor

    def __init__(self, name, hostname, port, username, password):
        self.name = name

        t = rnd.normalvariate(5,2)
        self.thF = threading.Timer(t,self.setFire)
        self.thF.start()
        
        t = rnd.normalvariate(5,2)
        self.thT = threading.Timer(t,self.tempSensor)
        self.thT.start()

        t = rnd.normalvariate(5,2)
        self.thS = threading.Timer(t,self.smokeSensor)
        self.thS.start()

        self.client = mqtt.Client(client_id=self.name)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(hostname, port, 60)

        self.client.loop_start()

    def cancel(self):
        self.thF.cancel()
        self.thT.cancel()
        self.thS.cancel()
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("firealarm/"+self.name+"/sprinkler")

    def on_message(self, client, userdata, msg):
        if (msg.topic == "firealarm/"+self.name+"/sprinkler"):
            if (msg.payload.decode("ascii") == "on"):
                self.setSprinkler(True)
            elif (msg.payload.decode("ascii") == "off"):
                self.setSprinkler(False)

    def setFire(self):
        p = rnd.random()
        if ((not self.fire) and (not self.sprinkler) and (p < 0.10)):
            self.fire = True
            print(self.name+" is on Fire")
        elif (self.fire) and (self.sprinkler) and (p < 0.4):
            self.fire = False
            print(self.name+" fire wents out")
        t = rnd.normalvariate(5,2)
        self.thF = threading.Timer(t,self.setFire)
        self.thF.start()

    def setSprinkler(self, status):
        self.sprinkler = status

    def tempSensor(self):
        if (not self.fire):
            self.temp = rnd.normalvariate(25,1)
        else:
            self.temp = rnd.normalvariate(57,4)
        self.client.publish("firealarm/"+self.name+"/temp",str(self.temp))
        t = rnd.normalvariate(5,2)
        self.thT = threading.Timer(t,self.tempSensor)
        self.thT.start()

    def smokeSensor(self):
        if (not self.fire):
            self.smoke = False
        else:
            self.smoke = True
        self.client.publish("firealarm/"+self.name+"/smoke",str(self.smoke))
        t = rnd.normalvariate(5,2)
        self.thS = threading.Timer(t,self.smokeSensor)
        self.thS.start()

if __name__ == "__main__":
    if (len(sys.argv) == 6):
        N = int(sys.argv[1])
        if (N < 1):
            print("Invalid number of rooms")
            exit(0)
        R = [None]*N
        print("Starting rooms...")
        for i in range(0,N):
            R[i] = Room(name="Room"+str(i+1),hostname=sys.argv[2],port=int(sys.argv[3]),username=sys.argv[4],password=sys.argv[5])
        print("Rooms are running, press any key to stop simulation")
        a = input()
        print("Stopping simulation...")
        for r in R:
            r.cancel()
        print("Done")
    else:
        print("Usage: python3 fire.py <N> <host> <port> <usr> <pswd>")
        print("N: the number of rooms to simulate")
        print("host: hostname of the MQTT broker")
        print("port: TCP port of the MQTT broker, don't use TLS/SSL port")
        print("usr: MQTT username")
        print("pswd: MQTT password")