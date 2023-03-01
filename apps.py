import json
import boto3
from urllib.request import urlopen
from datetime import datetime

def f(event,context):
    with urlopen("https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario") as response:
        data = response.read()

    client = boto3.client("s3")
    client.put_object(Body=data, Bucket="raw-dolar-despliegue-roxy", Key="dolar-despliegue-roxy.txt")

    s3 = boto3.resource('s3')
    bucket = s3.Bucket("raw-dolar-despliegue-roxy")
    obj = bucket.Object("dolar-despliegue-roxy.txt")
    body = obj.get()['Body'].read()
    body = json.loads(body)

    s ="fecha,valor\n"

    for item in body:
        aux = item[0]
        aux = aux[:len(aux)-3]
        aux = datetime.fromtimestamp(int(aux), tz=None)
        s+= "{},{}\n".format(aux, item[1])

    client.put_object(Body=s, Bucket="dolar-despliegue-roxy", Key="dolar_timestamp.csv")

    print(s)

    return {
        'statusCode':201,
        'body': json.dumps("Data scrapped successfully :3.")
    }