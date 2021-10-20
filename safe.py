import base64
import typing

import click
import gnupg

_KEYS_SERVER = 'keyserver.ubuntu.com'
_DOMAIN = 'ioet.com'
_KEY_TYPE = 'RSA'
_KEY_LENGTH = 1024


class Key(typing.NamedTuple):
    key_id: str
    owner: str
    email: str


class KeyStorage:
    def __init__(self, gpg):
        self.gpg = gpg
    
    def create_key(self, username: str, name: str, last_name: str):
        input_data = self.gpg.gen_key_input(
            key_type=_KEY_TYPE,
            key_length=_KEY_LENGTH,
            name_real=f'{name} {last_name}',
            name_email=f'{username}@{_DOMAIN}',
        )
        key = self.gpg.gen_key(input_data)
        self.gpg.send_keys(_KEYS_SERVER, key.fingerprint)

    def list_all_keys(self) -> typing.List[Key]:
        public_keys = self.gpg.search_keys(f'*@{_DOMAIN}', _KEYS_SERVER)
        return [
            Key(
                key_id=each_key['keyid'],
                owner=each_key['uids'][0].split('<')[0].rstrip(),
                email=each_key['uids'][0].split('<')[1].split('>')[0],
            )
            for each_key in public_keys
        ]

    def get_key(self, email: str) -> Key:
        public_keys = self.gpg.search_keys(f'{email}@{_DOMAIN}', _KEYS_SERVER)

        if not public_keys:
            raise Exception(f'Key for user with email: {email} not found')

        return Key(
            key_id=public_keys[0]['keyid'],
            owner=public_keys[0]['uids'][0].split('<')[0].rstrip(),
            email=public_keys[0]['uids'][0].split('<')[1].split('>')[0],
        )


def _create_key(username: str, name: str, last_name: str):
    key_storage = KeyStorage(gnupg.GPG())
    key_storage.create_key(username, name, last_name)


def _encrypt_message(message: str, destination_email: str) -> str:
    gpg = gnupg.GPG()
    key_storage = KeyStorage(gpg)
    key = key_storage.get_key(destination_email)
    encryted_message = gpg.encrypt(message, [key.key_id])
    base_64_message = base64.b64encode(encryted_message.data)
    return base_64_message.decode('utf-8')


def _decrypt_message(encrypted_message: str) -> str:
    gpg = gnupg.GPG()
    encrypted_data = base64.b64decode(encrypted_message)
    decrypted_message = gpg.decrypt(encrypted_data)
    return decrypted_message.data.decode('latin1')


@click.command()
@click.option("--ioet-username", "-u")
@click.option("--name", "-n")
@click.option("--last-name", "-l")
def start(ioet_username, name, last_name):
    _create_key(ioet_username, name, last_name)
    click.echo('Your public key has been created')


@click.command()
@click.option("--text", "-t")
@click.option("--destination-email", "-e")
def encrypt(text, destination_email):
    click.echo(_encrypt_message(text, destination_email))


@click.command()
@click.option("--text", "-t")
def decrypt(text):
    click.echo(_decrypt_message(text))


@click.group()
def entry_point():
    pass

entry_point.add_command(start)
entry_point.add_command(encrypt)
entry_point.add_command(decrypt)


if __name__ == "__main__":
    entry_point()
