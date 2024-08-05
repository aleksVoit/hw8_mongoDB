from models import Contact
import connect
from producer import generate_contacts


def update_contact_preference():
    contacts = Contact.objects().all()
    for contact in contacts:
        contact.update()
        print(contact)


def delete_contacts():
    contacts = Contact.objects().all()
    for contact in contacts:
        contact.delete()
        print(f'{contact} was deleted')


if __name__ == '__main__':
    # pass
    # update_contact_preference()
    generate_contacts(10)
    # delete_contacts()
