import time
from database.db_utils import obtener_ips, actualizar_ip, insertar_metricas
from servicio.ping_controlador import ping
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

def iniciar():
    
    INTERVALO_MINUTOS = 10 

    while True:

         print("\n--- Iniciando monitoreo ---")

         dispositivos = obtener_ips(conexion)
 
                    
         for id_dispositivo, ip_actual in dispositivos:

             print(f"\nAnalizando →{ip_actual}")

             # Guarda en variables los resultados del ping
             fecha_ping, minimo, maximo, promedio, perdidos, disponible, enviados, recibidos, porcentaje = ping(ip_actual)
             
             # Llamada a la función que inserta los valores de la métricas en la base de datos
             insertar_metricas(conexion, id_dispositivo, fecha_ping, promedio, porcentaje, disponible)
             
            # Llamada a la función que evalúa las métricas para determinar el estado del dispositivo
             evaluar_metricas(conexion, id_dispositivo, fecha_ping, promedio, porcentaje, disponible)

         print(f"El proximo monitoreo se realizara en {INTERVALO_MINUTOS} minutos...")
         time.sleep(INTERVALO_MINUTOS * 60)