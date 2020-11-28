class Crypt:
    key = "}>CX[JAnpm8)H[rKEvrt/kse1G'j{Pd\jxfTNCxU/b4i0MeeV9A(FusO9zd9bM\m"
    splitter = "z"

    @staticmethod
    def de(inputed_str):
        decrypted = ""
        encrypted_list = inputed_str[:-1].split(Crypt.splitter)

        index = 0
        for num in encrypted_list:
            try:
                decrypted += chr(int(int(num) / ord(Crypt.key[index])))
            except IndexError:
                decrypted += chr(int(int(num) / ord(Crypt.key[index % 64])))
            finally:
                index += 1

        return decrypted

    @staticmethod
    def en(string):
        index = 0
        encrypted = ""
        for alpha in string:
            try:
                encrypted += str(ord(alpha) * ord(Crypt.key[index])) + Crypt.splitter
            except IndexError:
                encrypted += str(ord(alpha) * ord(Crypt.key[index % 64])) + Crypt.splitter
            finally:
                index += 1
        return encrypted
