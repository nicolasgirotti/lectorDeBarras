import mysql.connector
import json

# Establecer la conexión a la base de datos
conexion = mysql.connector.connect(
    host='localhost',
    user='nicolas',
    password='naiki2353',
    database='productos'
)

if conexion.is_connected():
    print('Conexión exitosa a la base de datos')

# Realizar operaciones con la base de datos
cursor = conexion.cursor()

archivo = '/home/parzival/Escritorio/productosContados.json'

# Abrir y cargar el archivo JSON
with open(archivo, 'r') as file:
    datos_productos = json.load(file)

# Iterar sobre los datos y realizar inserciones
for producto in datos_productos:
    nombre = producto['nameComplete']
    ean = producto['ean']
    tamaño = producto.get('tamaño')
    if isinstance(tamaño, dict):  # Verifica si 'tamaño' es un diccionario
        tamaño_valor = tamaño.get('valor')
        unidad = tamaño.get('unidad')
    else:
        tamaño_valor = 'None'
        unidad = 'None'
    
    precio = 0  # Asume un valor por defecto, podrías obtenerlo de otro lugar si es necesario

    # Insertar el producto en la base de datos
    insert_query = "INSERT IGNORE INTO lista_de_productos (ean, nameComplete, dimension, unidad_de_peso, precio) VALUES (%s, %s, %s, %s, %s)"
    datos = (ean, nombre, tamaño_valor, unidad, precio)

    cursor.execute(insert_query, datos)
    conexion.commit()

# Cerrar la conexión
cursor.close()
conexion.close()