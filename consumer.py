import pika
import json
from services import send_email
from models import Contact
import connect


def callback(ch, method, properties, body):
    email_data = json.loads(body)
    contact_id = email_data['contact_id']
    message = email_data['message']

    contact = Contact.objects(id=contact_id).first()
    email = contact.email
    name = contact.fullname
    try:
        send_email(email, message)
        contact.send_email = True
        print(f'Message - {message} was sent to {name} on {email}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as ex:
        print(f"Failed to process message: {ex}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue='send_email', durable=True)
    print(f'[*] Waiting for messages, to exit use Ctrl+C')

    channel.basic_qos(prefetch_count=5)
    channel.basic_consume(queue='send_email', on_message_callback=callback)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()




