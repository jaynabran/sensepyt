import machine
import time
import network
#from umqtt.simple import MQTTClient
import ujson
import urequests

#Config de la red
SSID = "ALEXIS 2.4_5GETB"
PASSWORD = "Bran-1997*/"

#Asigna Pines
SENSOR1_MOV_PIN = 13
LED1_PIN = 2

#Conexion WiFi
def wifiConnect():
    wifiSensePy = network.WLAN(network.STA_IF)
    if not wifiSensePy.isconnected():
        wifiSensePy.active(True)
        wifiSensePy.connect(SSID, PASSWORD)
        while not wifiSensePy.isconnected():
            pass
    print("Conectado a:", SSID)
    print("Info de red:", wifiSensePy.ifconfig())
    
#LA PARTE DE TELEGRAM
    
#Sensor_1 de movimiento
def mov1_sensor(pin):
    if pin.value() == 1:
        print("Se ha detectado un movimiento.")
        machine.Pin(LED1_PIN, machine.Pin.OUT).on()
        time.sleep(10)
        #notificacion
    else:
        print("Todo chevere!!!")
        machine.Pin(LED1_PIN, machine.Pin.OUT).off()
        time.sleep(5)
        
#Config pines
def configPines():
    machine.Pin(SENSOR1_MOV_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN).irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=mov1_sensor)
    machine.Pin(LED1_PIN,machine.Pin.OUT).off()
    
#Config de start
def setup():
    wifiConnect()
    configPines()
    
setup()

#Bucle
while True:
    pass