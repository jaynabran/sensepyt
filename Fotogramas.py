import camera
import uasyncio as asyncio
import machine
import uos

# Inicializa la cámara
camera.init(0, format=camera.JPEG) 
camera.quality(12)
camera.framesize(9)

# Inicializa la tarjeta microSD


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
loop = asyncio.get_event_loop()
video_frames = loop.run_until_complete(capture_video())
loop.close()

# Verifica si se tomaron los 10 fotogramas
if len(video_frames) == 10:
    print("Se capturaron los 10 fotogramas.")
    for i, frame in enumerate(video_frames):
        filename = f"frame_{i}.jpg"
        save_photo_to_sd(frame, filename)
        
else:
    print("No se capturaron los 10 fotogramas. Se capturaron:", len(video_frames), "fotogramas.")
    for i, frame in enumerate(video_frames):
        filename = f"frame_{i}.jpg"
        save_photo_to_sd(frame, filename)
        
