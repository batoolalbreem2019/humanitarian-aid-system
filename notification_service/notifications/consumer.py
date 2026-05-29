import json, pika, django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')
django.setup()
from django.conf import settings
from .models import Notification

def send_notification(user_id, request_id, ntype, message):
    Notification.objects.create(
        user_id=user_id, request_id=request_id,
        type=ntype, message=message
    )
    print(f"Notification sent to user {user_id}: {message}")

def start_consumer():
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue='aid_events', durable=True)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        data = event.get('data', {})
        ename = event.get('event')
        uid = data.get('user_id')
        rid = data.get('request_id')
        if ename == 'AidRequestApproved':
            send_notification(uid, rid, 'AID_APPROVED',
                f"Your aid request {rid} has been approved.")
        elif ename == 'AidRequestStatusChanged':
            send_notification(uid, rid, 'AID_APPROVED',
                f"Your aid request status changed to {data.get('new_status')}.")
        elif ename == 'AidDelivered':
            send_notification(uid, rid, 'AID_DELIVERED',
                f"Your aid request {rid} has been delivered.")
        elif ename == 'DonationReceived':
            send_notification(uid, None, 'DONATION_RECEIVED',
                "Thank you! Your donation has been received.")

    channel.basic_consume(queue='aid_events', on_message_callback=callback, auto_ack=True)
    print("Notification Service: listening for events...")
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()
