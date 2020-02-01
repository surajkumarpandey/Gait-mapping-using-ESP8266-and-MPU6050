
from pyqtgraph.Qt import QtGui,QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.ptime import time
import sys
#import serial
import codecs
import paho.mqtt.client as mqtt
import threading
import datetime
import time



now = datetime.datetime.now()
print(now)
ts = str(now)


datum=[0,0,0,0,0,0]
client = mqtt.Client()
def on_connect(client, userdata, flags, rc):
  client.subscribe("test")	
  	
	
def on_message(client, userdata, msg):
  global datum
  datum=np.array(msg.payload.decode().strip('][').split(',')).astype(np.float)

def mq():
	client.connect("MQTT_BROKER_ADDRESS",1883,60)
	client.on_connect = on_connect
	client.on_message = on_message
	client.loop_forever()

mqthread=threading.Thread(target=mq)
mqthread.start()
app = QtGui.QApplication([])
p=pg.plot()
p.setWindowTitle('Live Plot from Serial')
p.setInteractive(True)
curve = p.plot(pen=(255,0,0), name="Red X curve")
curve2 = p.plot(pen=(0,255,0), name="Green Y curve")
curve3 = p.plot(pen=(0,0,255), name="Blue Z curve")
data = [0]
data2 = [0]
data3 = [0]
scroll=0
def update():
    global curve, data, curve2, data2, curve3, data3,scroll
    R = int(datum[0])
    G = int(datum[1])
    B = int(datum[3]*20)    
    scroll+=1
    if scroll<= 1200:
        data.append(int(R))
        data2.append(int(G))
        data3.append(int(B))
    else:
        data=data[1:]
        data.append(R)
        data2=data2[1:]
        data2.append(G)
        data3=data3[1:]
        data3.append(B)
    
    curve.setData(data)
    curve2.setData(data2)
    curve3.setData(data3)
    app.processEvents()
    if (float(datum[0])>180.0):
        timer.stop()
        exporter = pg.exporters.ImageExporter(p.plotItem)
        exporter.parameters()['width'] = 2000
        exporter.export("SAVE_PLOT_PATH"+ts+".jpeg")
        client.disconnect()
        app.closeAllWindows()		

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
mqthread.join()  
