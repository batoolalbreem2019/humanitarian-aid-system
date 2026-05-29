import json, pika
from django.conf import settings

def publish_event(event_name, payload):
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue='aid_events', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='aid_events',
            body=json.dumps({'event': event_name, 'data': payload})
        )
        connection.close()
        print(f"Event published: {event_name}")
    except Exception as e:
        print(f"Failed to publish event: {e}")
