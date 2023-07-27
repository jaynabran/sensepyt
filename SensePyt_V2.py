import machine
import time
import network
import ujson
import urequests as requests
import camera
import uos
from machine import Pin, ADC, PWM
from machine import UART
import uasyncio as asyncio


#Datos Bot telegram
CHAT_ID = "5321453259" #mio
#CHAT_ID = "-863734460" #Grupo
TOKEN = "6367476178:AAFvyXryIcCb5SX193RGGh30t7sPsoxABuE"

#Config de la red
SSID = "ALEXIS 2.4_5GETB"
PASSWORD = "Bran-1997*/"

#Conexion Wifi
def wifiConnect():
    wifiSensePy = network.WLAN(network.STA_IF)
    if not wifiSensePy.isconnected():
        wifiSensePy.active(True)
        wifiSensePy.connect(SSID, PASSWORD)
        while not wifiSensePy.isconnected():
            pass
    print("Conectado a:", SSID)
    print("Info de red:", wifiSensePy.ifconfig())

# Inicializa la cámara
camera.init(0, format=camera.JPEG) 
camera.quality(12)
camera.framesize(9)


async def capture_video():
    frames = []
    for i in range(10):  # Captura 10 fotogramas para formar el video
        frame = camera.capture()
        if isinstance(frame, bytes):
            frames.append(frame)
        await asyncio.sleep_ms(100)  # Espera 100 ms entre cada fotograma
    return frames

def save_photo_to_sd(photo, filename):
    with open("/sd/" + filename, "wb") as f:
        f.write(photo)
    print("Fotograma guardado:", filename)

#connect_wifi(ssid, password)


#Asigna Pines
INTERRUPTOR1_PIN = 12
SENSOR_MOVIMIENTO_PIN = 13
LED_PIN = 2
INTERRUPTOR2_PIN = 15
BUZZER_PIN = 14

#Start de pines
led = Pin(LED_PIN, Pin.OUT)
sensor_movimiento = Pin(SENSOR_MOVIMIENTO_PIN, Pin.IN)
interruptor1 = Pin(INTERRUPTOR1_PIN, Pin.IN, machine.Pin.PULL_DOWN)
interruptor2 = Pin(INTERRUPTOR2_PIN, Pin.IN, machine.Pin.PULL_DOWN)
buzzer = PWM(Pin(BUZZER_PIN),freq=260)

# Función para activar el buzzer y enviar una notificación a través de Telegram
def activate_buzzer():
    buzzer.duty(3)
    notif_Telegram("¡Se han abierto los contadores!")
    time.sleep(2)

# Función para desactivar el buzzer
def deactivate_buzzer():
    buzzer.duty(0)

#Notificacion a Telegram
def notif_Telegram(message):
    url = "https://api.telegram.org/bot" + TOKEN + "/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=data)
    return response.json()

# Bucle principal
def entrada():
    while True:
        if sensor_movimiento.value() == 1 or interruptor1.value() == 0:
        #if interruptor1.value() == 0:
            led.value(1)
            #led.on()
            print("Se ha detectado un movimiento.")
            notif_Telegram("¡Se ha detectado una intrusion!!!!")
            loop = asyncio.get_event_loop()
            video_frames = loop.run_until_complete(capture_video())
            loop.close()
            # Verifica si se tomaron los 10 fotogramas
            if len(video_frames) == 10:
                print("Se capturaron los 10 fotogramas.")
                for i, frame in enumerate(video_frames):
                    filename = f"frame_{i}.jpg"
                    save_photo_to_sd(frame, filename)
                    break
            else:
                print("No se capturaron los 10 fotogramas. Se capturaron:", len(video_frames), "fotogramas.")
                for i, frame in enumerate(video_frames):
                    filename = f"frame_{i}.jpg"
                    save_photo_to_sd(frame, filename)
                    break    
            time.sleep(5)
            break
        else:
            led.value(0)
            print("Todo bien.")
            time.sleep(2)
            break

def contadores():
    while True:
        if interruptor2.value() == 0:
            print("Apertura de contadores")
            activate_buzzer()            
            time.sleep(2)
            break
        else:
            led.value(0)
            print("Contadores cerrados.")
            deactivate_buzzer()
            time.sleep(2)
            break
    
def setup():
    wifiConnect()
    contadores()
    entrada()


#Bucle
while True:
    setup()
    pass