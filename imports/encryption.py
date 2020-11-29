from cryptography.fernet import *


class Crypt:
    key = b'E0kGTj9oe68mgUnNZuMwfzosAWO4C1YiO_EIBsaQcTw='

    @staticmethod
    def de(input_str):
        return Fernet(Crypt.key).decrypt(input_str.encode()).decode()

    @staticmethod
    def en(input_string):
        return Fernet(Crypt.key).encrypt(input_string.encode()).decode()
