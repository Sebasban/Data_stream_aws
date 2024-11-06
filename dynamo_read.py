import boto3

# Crear un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

# Nombre de la tabla
table_name = 'Inventary_data'

# Realizar un escaneo completo de la tabla
response = dynamodb.scan(
    TableName=table_name
)

# Mostrar los ítems encontrados
for item in response.get('Items', []):
    print(item)
