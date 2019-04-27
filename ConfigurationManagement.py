import tftpy
import os.path as path
import os
import filecmp
import shutil
import threading
import time
from SNMPget import getSNMP

ips = {"50.0.0.1"}
inventario = {}
mib = "1.3.6.1.2.1.1.1.0"

routers = {"r1": "50.0.0.1"}

def obtenerConfiguraciones():
    while 1:
        for router, direccion in routers.items():
            try:
                if path.exists(router):
                    tftpy.TftpClient(direccion, 69).download('startup-config', router + "-temp")
                    f = open(router)
                    ftemp = open(router + "-temp")
                    filecmp.clear_cache()
                    if not f.readlines() == ftemp.readlines():  # Regresa true si son iguales
                        print("Cambios detectados en el archivo: " + router)
                        shutil.move(router + "-temp", router)
                    else:
                        os.remove(router + "-temp")
                else:
                    tftpy.TftpClient(direccion, 69).download('startup-config', router)

            except:
                print("Falló la comunicación con " + router + ":" + direccion)

        time.sleep(10)

def obtenerInventario():
    resultado = []
    for ip in ips:
        sysDesc = getSNMP(ip, "demo", "password", mib)
        if sysDesc != "ERROR":
            resultado.append([ip,sysDesc])
    return resultado

def mostrarInventario(inventario):
    f = open("inventario", mode="w")
    for ip, descr in inventario:
        f.write("\n" + ip + ":\n" + descr + "\n")
        print("\n" + ip + ":\n" + descr + "\n")


mostrarInventario(obtenerInventario())
obtenerConfiguraciones()