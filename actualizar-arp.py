from arp_scanner import obtener_tabla_arp
from database.config import Config
import MySQLdb

def obtener_mac_db():
    conexion = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        charset="utf8"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT id_dispositivo, mac_address, ip_actual FROM dispositivo")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def actualizar_ip(id_dispositivo, nueva_ip):
    conexion = MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB,
        charset="utf8"
    )
    cursor = conexion.cursor()

    sql = "UPDATE dispositivo SET ip_actual=%s WHERE id_dispositivo=%s"
    cursor.execute(sql, (nueva_ip, id_dispositivo))

    conexion.commit()
    cursor.close()
    conexion.close()


def actualizar_ips_por_arp():
    tabla_arp = obtener_tabla_arp()
    dispositivos = obtener_mac_db()

    for id_disp, mac, ip_actual in dispositivos:
        mac = mac.lower()

        if mac in tabla_arp:
            nueva_ip = tabla_arp[mac]

            if nueva_ip != ip_actual:
                print(f"🔄 IP cambiada para {mac}: {ip_actual} → {nueva_ip}")
                actualizar_ip(id_disp, nueva_ip)
            else:
                print(f"✔ {mac} sigue con la misma IP ({ip_actual})")
        else:
            print(f"⚠ {mac} no aparece en la tabla ARP (dispositivo apagado o fuera de VLAN)")