import boto3
import time

# Configura el cliente de Kinesis
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
STREAM_NAME = 'django_proyecto'  # Reemplaza con el nombre de tu stream

# Obtén el Shard ID
shard_response = kinesis_client.describe_stream(StreamName=STREAM_NAME)
shard_id = shard_response['StreamDescription']['Shards'][2]['ShardId']

# Obtén el Shard Iterator
iterator_response = kinesis_client.get_shard_iterator(
    StreamName=STREAM_NAME,
    ShardId=shard_id,
    ShardIteratorType='LATEST'  # Cambiar a LATEST para ver los registros más recientes
)
shard_iterator = iterator_response['ShardIterator']
print(shard_id)
# Lee registros hasta que se obtenga una respuesta no vacía
while True:
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)
    records = records_response['Records']
    print(records)
    
    if records:
        for record in records:
            print(record['Data'].decode('utf-8'))  # Decodifica los datos de bytes a string
    else:
        print("No hay registros disponibles en este momento.")
    
    # Actualiza el shard iterator
    shard_iterator = records_response['NextShardIterator']
    
    # Espera un segundo antes de volver a intentar
    time.sleep(1)
