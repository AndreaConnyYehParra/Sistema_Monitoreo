import MySQLdb
import subprocess
from database.db_utils import obtener_ips
from database.config import Config
from datetime import datetime   


def obtener_ip():
    
    conexion = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        charset='utf8'
    )

    ips=obtener_ips(conexion)
    conexion.close()
    
    ip = [ips[2] for ips in ips]
    return ip



def ping(ip):

    comando = ["ping", "-n", "4", "-w", "1000", ip]

    try:
        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Convertir salida a texto
        salida = resultado.stdout.decode("cp850")
        
        #Establece valores por defecto
        disponible = (resultado.returncode == 0)
        paquetes = "No encontrado"
        minimo = maximo = promedio = "0"

        # Analizar líneas del ping
        for linea in salida.splitlines():

            # Paquetes:
            if "Paquetes" in linea:
                paquetes = linea.replace("Paquetes: ", "").split(",")
                if len(paquetes) >= 3:
                    enviados = paquetes[0].split("=")[1].strip()
                    recibidos = paquetes[1].split("=")[1].strip()
                    perdidos = paquetes[2].split("=")[1].strip()
                    
            # Tiempos:
            if "Mínimo" in linea:
                latencia = linea.replace("ms", "").split(",")
                if len(latencia) >= 3:
                   minimo = latencia[0].split("=")[1].strip()
                   maximo = latencia[1].split("=")[1].strip()
                   promedio = latencia[2].split("=")[1].strip()
        
        fecha_ping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        print(f"\nFecha: {fecha_ping}")   
        print(f"\nIP: {ip}")
        print(f"Paquetes → Min: {enviados} | Recibidos: {recibidos}| Perdidos: {perdidos}")
        print(f"Latencia → Min: {minimo} ms | Max: {maximo} ms | Promedio: {promedio} ms")

        return resultado.returncode == 0

    except Exception as e:
        print("Error:", e)
        return False
    


if __name__ == "__main__":
    lista_ips = obtener_ip()

    print("IPs encontradas:", lista_ips)

    for ip in lista_ips:
        estado = ping(ip)
        if estado:
            print("Estado: Disponible")
        else:
            print("Estado: No disponible")