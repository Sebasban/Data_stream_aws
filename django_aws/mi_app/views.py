from django.shortcuts import render
from django.http import HttpResponse
import boto3
import json
from botocore.exceptions import ClientError
from datetime import datetime

kinesis_client = boto3.client('kinesis', region_name='us-east-1')  # Asegúrate de que la región sea la correcta
STREAM_NAME = 'django_proyecto'  # Reemplaza con el nombre de tu stream

def index(request):
    if request.method == 'POST':
        if 'accion' in request.POST:
            producto = request.POST.get('Producto')  # Captura el valor del primer campo
            cantidad = request.POST.get('Cantidad')  # Captura el valor del segundo campo
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            # Aquí puedes hacer algo con los valores capturados, como guardarlos en la base de datos
            data = {
                    'producto': producto,
                    'cantidad': cantidad,
                    'fecha': fecha_actual
                }
            try:
                response = kinesis_client.put_record(
                    StreamName=STREAM_NAME,
                    Data=json.dumps(data),  # Convierte los datos a JSON
                    PartitionKey='fecha'  # Puedes usar una clave de partición adecuada
                )
                return HttpResponse(f'Datos almacenados en Kinesis: {data}, Response: {response}')
            except ClientError as e:
                return HttpResponse(f'Error al enviar a Kinesis: {e}')
    return render(request, 'index.html')
