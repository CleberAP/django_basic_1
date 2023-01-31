# Fonte: https://morioh.com/p/4f5288b77c14

from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key() 

def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        encoder = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = encoder.encrypt(txt.encode('utf-8'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("utf-8") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return e #None

def decrypt(txt):
    try:
        # base64 decode
        bytes_txt = bytes(txt, 'utf-8') #base64.urlsafe_b64decode(txt)
        token_decoder = Fernet(settings.ENCRYPT_KEY)
        decoded_text = token_decoder.decrypt(bytes_txt).decode("utf-8")     
        return decoded_text
        
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return e #None
