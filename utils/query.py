import psycopg2
from psycopg2 import Error
from django.conf import settings

try:
    # Connect ke db
    connection = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

    curr = connection.cursor()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    