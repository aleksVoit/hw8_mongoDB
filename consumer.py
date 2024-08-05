import pika
import json
from services import send_email, send_sms
from models import Contact
import connect


def email_callback(ch, method, properties, body):
    email_data = json.loads(body)
    contact_id = email_data['contact_id']
    message = email_data['message']

    contact = Contact.objects(id=contact_id).first()
    email = contact.email
    name = contact.fullname
    try:
        send_email(email, message)
        contact.send_msg = True
        contact.save()
        print(f'Message - {message} was sent to {name} on {email}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as ex:
        print(f"Failed to process message: {ex}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def sms_callback(ch, method, properties, body):
    email_data = json.loads(body)
    contact_id = email_data['contact_id']
    message = email_data['message']

    contact = Contact.objects(id=contact_id).first()
    phone = contact.phone_number
    name = contact.fullname
    try:
        send_sms(phone, message)
        contact.send_msg = True
        contact.save()
        print(f'Message - {message} was sent to {name} on {phone}')
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
    print(f'[*] Waiting for messages, to exit use Ctrl+C')

    email_channel = connection.channel()
    email_channel.queue_declare(queue='send_email', durable=True)
    email_channel.basic_qos(prefetch_count=1)
    email_channel.basic_consume(queue='send_email', on_message_callback=email_callback)

    sms_channel = connection.channel()
    sms_channel.queue_declare(queue='send_sms', durable=True)
    sms_channel.basic_qos(prefetch_count=1)
    sms_channel.basic_consume(queue='send_sms', on_message_callback=sms_callback)
    try:
        sms_channel.start_consuming()
        email_channel.start_consuming()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()




