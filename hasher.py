import sys
import hashlib

def main(argv):
    if len(argv) != 1:
        print('Need to provide password to hash as argument.')
        print('python3 hasher.py your-password-here')
        print('I would suggest piping the output to a file to be copied later to root owned secret file:')
        print('python3 hasher.py your-password-here > tmpstore.txt')
        print('As root, make sure you store the created hash in the secret file owned by root, and only readable by root:')
        print('sudo touch secretfile')
        print('sudo vi secretfile (place hash at this point)')
        print('sudo chmod 400 secretfile (locks secret file from only being readable as root)')
        print('Then store your password in a root owned, readonly by root configuration file.')
        sys.exit(1)

    pw = argv[0].encode('ascii')
    hashed_password = hashlib.sha512(pw).hexdigest()
    print(hashed_password)

if __name__ == '__main__':
    main(sys.argv[1:])
