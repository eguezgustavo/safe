# Safe
Safe is a small utility to encrypt and decrypt messages using a pair of public and private keys.

## Installation
You need to have GPG installed in your machine. Please follow this link: https://blog.ghostinthemachines.com/2015/03/01/how-to-use-gpg-command-line/


To start clone this repository and run
```
make install
```

After that, generate a pair of keys by using this command:
```
safe start --ioet-username <your_username> --name <Your First Name> --last-name <Your Last Name> 
```

## Encrypt a messages
```
safe encrypt --text "this is a message" --destination-email "some@email.mail"
```

## Decrypt a messages
```
safe decrypt --text "<some encrypted string>"
```