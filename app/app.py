from flask import Flask, render_template, request, jsonify, redirect, Response
from pyzbar import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol
import base64, cv2
from PIL import Image
import io

app = Flask(__name__)


@app.route('/')
def capturar():
    return render_template('index.html')

# Captura el codigo en tiempo real
def generar_frames():
    # Inicia la captura de la camara
    cam = cv2.VideoCapture(0)
    
    # Bucle de captura de fotogramas
    while True:
        # En OpenCV, al utilizar el metodo read se devuelven dos valores
        # ret -> Booleano que indica si la captura del fotograma fue exitosa.
        # frame -> es una matriz de numpy que contiene la imagen
        ret, frame = cam.read()
        if not ret:
            break
        else:
            # Procesamiento del fotograma:
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convierte el fotograma a escala de grises.
            
            codigos = decode(gray) 
            # Itera sobre los codigos encontrados decodificados
            for codigo in codigos:
                print("Código:", codigo.data.decode('utf-8'))
            
            # Codificacion y transmision de imagen
            
            # Convierte el fotograma original a formato JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            
            # Convierte la imagen codificada en bytes 
            frame = buffer.tobytes()
            
            # Genera y devuelve el fotograma codificado como un flujo de datos multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video_feed')
def video_feed():
    return Response(generar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)