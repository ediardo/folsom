from keystoneclient.auth import identity
from backend.credentials import get_keystone_creds
from backend.credentials import get_barbicankey_ref
from keystoneclient import session
from barbicanclient import client
from cryptography.fernet import Fernet


def bootstrap_clients():
    creds = get_keystone_creds()
    auth = identity.v3.Password(**creds)
    sess = session.Session(auth=auth)
    barbican = client.Client(session=sess)
    return barbican


def encrypt_fernet(data):
    success = False
    while not success:
        try:
            print "clear_text:" + data
            barbican = bootstrap_clients()
            key_href = get_barbicankey_ref()
            print "key_href:" + key_href
            key = retrieve_stored_secret(barbican, key_href)
            print "key:" + key
            cipher_suite = Fernet(key)
            cipher_text = cipher_suite.encrypt(data)
            print "cipher_text:" + cipher_text
            success = True
            return cipher_text
        except Exception as e:
            print(e)
            pass


def decrypt_fernet(cipher_text):
    success = False
    i = 0
    while not success and i < 5:
        try:
            print "cipher_text:" + cipher_text
            barbican = bootstrap_clients()
            key_href = get_barbicankey_ref()
            print "key_href:" + key_href
            key = retrieve_stored_secret(barbican, key_href)
            print "key:" + key
            cipher_suite = Fernet(key)
            plain_text = cipher_suite.decrypt(cipher_text)
            print "clear_text:" + plain_text
            success = True
            return plain_text
        except Exception as e:
            i += 1
            pass

        raise Exception("Couldn't decrypt!")


def retrieve_stored_secret(barbican, my_secret_ref):
    # Retrieve Secret from secret reference
    retrieved_secret = barbican.secrets.get(my_secret_ref)
    fernet_key = retrieved_secret.payload
    return fernet_key


if __name__ == "__main__":
    data = 'so freaking secret'
    cipher_text = encrypt_fernet(data)
    # cipher_text = 'gAAAAABYEZ7IYbyg86ZoFPnq7_Tou_iKwa5tvCjTYlwa4K5tdlfdFWgLYWwH2UCWeqooMK4URHGdwdQnaQ6HjJy5Lq0kold9jxT4WGp19EQSTgE6VhYeAyk='
    decrypt_fernet(cipher_text)
