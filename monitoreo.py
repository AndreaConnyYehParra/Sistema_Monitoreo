import time
from database.db_utils import obtener_ips, actualizar_ip, insertar_metricas
from servicio.ping_controlador import ping
from servicio.arp_controlador import obtener_tabla_arp, buscar_ip
from servicio.evaluar_metricas import evaluar_metricas

import MySQLdb
from database.config import Config

conexion = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        charset='utf8'
    )


INTERVALO_MINUTOS = 5

#while True:
print("\n--- Iniciando monitoreo ---")

    #Almacenar direccion ip y mac de la funcion obtener_ips de db_utils
dispositivos = obtener_ips(conexion)
#Almacenar la tabla arp de arp_controlador
arp = obtener_tabla_arp()
print(arp)
    
for id_dispositivo, macadd, ip_actual in dispositivos:

        print(f"\nAnalizando →{ip_actual}")

        # Realiza un ping 
        fecha_ping, minimo, maximo, promedio, perdidos, disponible, enviados, recibidos = ping(ip_actual)
        
        # Busca en la tabla arp la mac y verifica si cambio la ip
        nueva_ip = buscar_ip(arp, macadd)
        print(f"Nueva ip: {nueva_ip}")

        #Si la nueva ip es diferente de la ip_actual, actualizar la ip en la base de datos
        if nueva_ip and nueva_ip != ip_actual:
            print(f"IP nueva detectada: {ip_actual} → {nueva_ip}")
            actualizar_ip(conexion, id_dispositivo, nueva_ip)
            ip_actual = nueva_ip

        # Insertar en los datos de latencia, disponibilidad y perdida de paquetes en la base de datos
        insertar_metricas(conexion, id_dispositivo, fecha_ping, promedio, perdidos, disponible)
        
        evaluar_metricas(conexion, id_dispositivo, fecha_ping, promedio, perdidos, disponible)

        #print(f"⏳ Esperando {INTERVALO_MINUTOS} minutos...")
        