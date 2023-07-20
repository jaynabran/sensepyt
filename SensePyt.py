import machine
import time
import network
#from umqtt.simple import MQTTClient
import ujson
import urequests as requests
from utelegram import Bot

#Bot telegram
CHAT_ID = "5321453259" #mio
#CHAT_ID = "-863734460" #Grupo
TOKEN = "6367476178:AAFvyXryIcCb5SX193RGGh30t7sPsoxABuE"
bot = Bot(TOKEN)

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
    
    
#Notificacion a Telegram
def notif_Telegram(message):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=data)
    return response.json()

#Sensor_1 de movimiento
def mov1_sensor(pin):
    if pin.value() == 1:
        print("Se ha detectado un movimiento.")
        machine.Pin(LED1_PIN, machine.Pin.OUT).on()
        notif_Telegram("ALV, ya valimos!!!")
        time.sleep(10)
        #notificacion
    else:
        print("Todo chevere!!!")
        machine.Pin(LED1_PIN, machine.Pin.OUT).off()
        notif_Telegram("Todo Cool!!!")
        time.sleep(5)
        
#Config pines
def configPines():
    machine.Pin(SENSOR1_MOV_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN).irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=mov1_sensor)
    machine.Pin(LED1_PIN,machine.Pin.OUT).off()
    
#Config de start
def setup():
    wifiConnect()
    #bot.start_loop()
    configPines()
        
setup()

#Bucle
while True:
    pass