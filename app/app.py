from flask import Flask, render_template, request, jsonify, redirect, Response, url_for, session
from flask_socketio import SocketIO, emit
from pyzbar import pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol
import base64, cv2
from PIL import Image
import io, threading
from collections import Counter



app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'
socketio = SocketIO(app, async_mode='eventlet')
barcode_found = False
codigoDeBarra = None


@app.route('/')
def capturar():
    return render_template('index.html')


# Captura el codigo en tiempo real
def generar_frames():
    global barcode_found
    global codigoDeBarra 
    # Inicia la captura de la camara
    cam = cv2.VideoCapture(0)
    lista_codigos = []
    
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
            
            codigos = decode(gray, symbols=[ZBarSymbol.EAN13]) 
            
            
            # Itera sobre los codigos encontrados decodificados
            for codigo in codigos:
                codigo_decodificado = codigo.data.decode('utf-8')
                print(codigo_decodificado)
                lista_codigos.append(codigo_decodificado)
                
                
            # Cuando captura 20 veces el codigo
            if len(lista_codigos) == 5:
                masProbable = calcularCodigo(lista_codigos)
                print(f"El numero mas probable es {masProbable}")
                lista_codigos= []
                barcode_found = True
                codigoDeBarra = masProbable
                break
               
           
            # Codificacion y transmision de imagen
            
            # Convierte el fotograma original a formato JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            
            # Convierte la imagen codificada en bytes 
            frame = buffer.tobytes()
            
            # Genera y devuelve el fotograma codificado como un flujo de datos multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if barcode_found:
            socketio.emit('redirect',{'url': '/codigoEAN'})

@socketio.on('connect')
def handle_connect():
    global barcode_found
    if not barcode_found:
        t = threading.Thread(target=generar_frames)
        t.start()
    else:
        emit('redirect', {'url': '/codigoEAN', 'codigoBarra': codigoDeBarra})


codigoValido = False

@app.route('/video_feed')
def video_feed():
    return Response(generar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    


def calcularCodigo(lista_codigo):
    contador_codigos = Counter(lista_codigo)
    masProbable = contador_codigos.most_common(1)[0][0]
    
    return masProbable


@app.route('/codigoEAN')
def codigoEAN():
    return render_template('codigo.html', codigo=codigoDeBarra)




if __name__ == '__main__':
    socketio.run(app, debug=True)