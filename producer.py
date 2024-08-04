import json

from faker import Faker
import connect
from models import Contact
import pika

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


def generate_contacts(quantity: int):
    faker = Faker()
    for _ in range(quantity):
        fullname = faker.name()
        email = faker.email()
        phone = faker.phone_number()
        Contact(fullname=fullname, email=email, phone_number=phone).save()


def get_contacts():
    contacts = Contact.objects().all()
    [print(contact.fullname) for contact in contacts]
    return contacts


def main():
    contacts = get_contacts()
    for contact in contacts:
        msg_data = {
            'contact_id': str(contact.id),
            'message': f'Hello {contact.fullname}! How are you?'
        }
        channel.basic_publish(
            exchange='email_mock',
            routing_key='send_email',
            body=json.dumps(msg_data).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
        print(f'send email to {contact.fullname}')
    connection.close()


if __name__ == '__main__':
    # generate_contacts(5)
    main()
