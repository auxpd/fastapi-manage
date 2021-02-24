import os
import sys


def main():
    command = 'fastapi-manage '
    command += ' '.join(sys.argv[1:])
    os.chdir(sys.path[0])
    os.system(command)


if __name__ == '__main__':
    main()
