import json
import boto3
from base64 import b64decode

# Crear el cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

# Nombre de la tabla de DynamoDB donde se insertarán los datos
dynamodb_table_name = 'Inventary_data'

def lambda_handler(event, context):
    print(f"El evento es:{event}")
    
    # Iteramos sobre los registros del evento
    for record in event['Records']:
        # Decodificamos el dato de Kinesis (contenido en base64)
        payload = json.loads(b64decode(record['kinesis']['data']).decode('utf-8'))
        print(f'este es el payload: {payload}')
        
        # Verificamos que el payload contiene las claves necesarias (producto, cantidad, fecha)
        if 'producto' in payload and 'cantidad' in payload and 'fecha' in payload:
            # Convertimos el payload en el formato requerido para DynamoDB
            item = {
                'product_id' : {'S': str(payload['producto'])},
                'producto': {'S': str(payload['producto'])},
                'cantidad': {'N': str(payload['cantidad'])},  # Es necesario convertir la cantidad a string para DynamoDB
                'fecha': {'S': str(payload['fecha'])}
            }
            
            # Insertamos el dato en la tabla de DynamoDB
            try:
                dynamodb.put_item(TableName=dynamodb_table_name, Item=item)
                print(f"Registro insertado: {item}")
            except Exception as e:
                print(f"Error al insertar el registro en DynamoDB: {e}")
        else:
            print("El payload recibido no contiene las claves esperadas: 'producto', 'cantidad' y 'fecha'")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Procesamiento de registros completo')
    }
