from models import Contact
from connect import connect


def get_contacts():
    contacts = Contact.objects().all()
    [print(contact.fullname) for contact in contacts]
    return contacts
