LOG_FILE = 'log.log'
HOST, PORT = "50.0.0.2", 514

import logging
import socketserver
from Email import send_notification
import subprocess

niveles = ["Emergencia", "Alerta", "Crítico", "Error", "Advertencia", "Notificación", "Información", "Debugging"]

logging.basicConfig(level=logging.DEBUG, format='%(message)s', datefmt='', filename=LOG_FILE, filemode='a')

#Obtiene el nivel del mensaje (0 a 7)
def obtenerNivel(mensaje_syslog):
    inicio = mensaje_syslog.find("<") + 1
    fin = mensaje_syslog.find(">")
    nivel = int(mensaje_syslog[inicio:fin]) % 8
    return niveles[nivel]

#Notifica por sistema
def notificar_sistema(mensaje):
    command = ['notify-send', mensaje]
    subprocess.call(command, stdout=False)

#Manda notificaciones por correo, sms y notifica por sistema
def notificar(mensaje_syslog):
    mensaje = obtenerNivel(mensaje_syslog)
    notificar_sistema(mensaje)


#Comportamiento del servidor UDP que recibirá los logs
class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        print( str(self.client_address[0]) + ": " + obtenerNivel(str(data)) + " -- " + str(data))
        notificar(str(data))
        logging.debug(str(data))


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")