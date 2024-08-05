import json

from faker import Faker
import connect
from models import Contact
import pika
from random import choice
from contacts_handlers import get_contacts

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
channel.exchange_declare(exchange='email_mock', exchange_type='direct')
channel.queue_declare(queue='send_email', durable=True)
channel.queue_bind(exchange='email_mock', queue='send_email')

channel.exchange_declare(exchange='sms_mock', exchange_type='direct')
channel.queue_declare(queue='send_sms', durable=True)
channel.queue_bind(exchange='sms_mock', queue='send_sms')


def generate_contacts(quantity: int):
    faker = Faker()
    preferences = ['email', 'sms']
    for _ in range(quantity):
        fullname = faker.name()
        email = faker.email()
        phone = faker.phone_number()
        Contact(fullname=fullname, email=email, phone_number=phone, preference=choice(preferences)).save()


def send_sms(contact, msg_data) -> None:
    channel.basic_publish(
        exchange='sms_mock',
        routing_key='send_sms',
        body=json.dumps(msg_data).encode(),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )
    print(f'send sms to {contact.fullname}')


def send_email(contact, msg_data) -> None:
    channel.basic_publish(
        exchange='email_mock',
        routing_key='send_email',
        body=json.dumps(msg_data).encode(),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )
    print(f'send email to {contact.fullname}')


def main():
    contacts = get_contacts()
    for contact in contacts:
        msg_data = {
            'contact_id': str(contact.id),
            'message': f'Hello {contact.fullname}! How are you?'
        }
        if contact.preference == 'sms':
            send_sms(contact, msg_data)
        elif contact.preference == 'email':
            send_email(contact, msg_data)
        else:
            send_email(contact, msg_data)
    connection.close()


if __name__ == '__main__':
    # generate_contacts(5)
    main()
