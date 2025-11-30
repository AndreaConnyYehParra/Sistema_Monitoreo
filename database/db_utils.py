
def obtener_tipos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("SELECT id_tipo, tipo_dispositivo FROM tipo")
    tipos = cursor.fetchall()
    cursor.close()
    return tipos

def obtener_ubicaciones(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("SELECT id_ubicacion, ubicacion FROM ubicacion")
    ubicaciones = cursor.fetchall()
    cursor.close()
    return ubicaciones

def obtener_dispositivos(conexion):
     cursor = conexion.connection.cursor()
     cursor.execute("""SELECT d.id_dispositivo, d.nombre_dispositivo,d.mac_address,d.ip_actual,t.tipo_dispositivo,u.ubicacion 
                    FROM dispositivo AS d
                    INNER JOIN tipo AS t
                    ON d.id_tipo_fk = t.id_tipo
                    INNER JOIN ubicacion AS u
                    ON d.id_ubicacion_fk = u.id_ubicacion
                    ORDER BY d.id_dispositivo ASC;""")
     dispositivos = cursor.fetchall()
     cursor.close()
     return dispositivos
 
def obtener_dispositivos_card(conexion, ubicacion):
    cursor = conexion.connection.cursor()
    if ubicacion==0:
        cursor.execute("""SELECT m.id_metrica, m.id_dispositivo_fk, d.nombre_dispositivo, d.mac_address, d.ip_actual,
                    m.latencia, m.paquetes_perdidos, m.disponibilidad, m.fecha
                    FROM metricas AS m
                    INNER JOIN dispositivo AS d
                    ON m.id_dispositivo_fk = d.id_dispositivo
                    WHERE m.fecha = (
                    SELECT MAX(m2.fecha)
                    FROM metricas AS m2
                    WHERE m2.id_dispositivo_fk = m.id_dispositivo_fk);""")
        dispositivos = cursor.fetchall()
        cursor.close()
        return dispositivos
    else:
        cursor.execute("""SELECT m.id_metrica, m.id_dispositivo_fk, d.nombre_dispositivo, d.mac_address, d.ip_actual,
                    m.latencia, m.paquetes_perdidos, m.disponibilidad, m.fecha, d.id_ubicacion_fk
                    FROM metricas AS m
                    INNER JOIN dispositivo AS d
                    ON m.id_dispositivo_fk = d.id_dispositivo
                    WHERE m.fecha = (
                    SELECT MAX(m2.fecha)
                    FROM metricas AS m2
                    WHERE m2.id_dispositivo_fk = m.id_dispositivo_fk) and id_ubicacion_fk=%s;""",(ubicacion,))
        dispositivos = cursor.fetchall()
        cursor.close()
        return dispositivos


def insertar_dispositivo(conexion, _nombre, _macadd, _ip_actual, _tipo, _ubicacion):
        cursor=conexion.connection.cursor()
        sql="INSERT INTO dispositivo (nombre_dispositivo,mac_address,ip_actual,id_tipo_fk,id_ubicacion_fk) VALUES (%s, %s, %s, %s, %s);"
        datos = (_nombre, _macadd, _ip_actual, _tipo, _ubicacion)
        cursor.execute(sql,datos)
        conexion.connection.commit()
        cursor.close()

def actualizar_dispositivo(conexion, _nombre, _macadd, _ip_actual, _tipo, _ubicacion, _id):
        cursor=conexion.connection.cursor()
        sql="UPDATE dispositivo SET nombre_dispositivo=%s,mac_address=%s,ip_actual=%s,id_tipo_fk=%s,id_ubicacion_fk=%s WHERE id_dispositivo=%s;"
        datos = (_nombre, _macadd, _ip_actual, _tipo, _ubicacion, _id)
        cursor.execute(sql,datos)
        conexion.connection.commit()
        cursor.close()

def eliminar_dispositivo(conexion,  id):
        cursor=conexion.connection.cursor()
        cursor.execute("DELETE FROM metricas WHERE id_dispositivo_fk = %s", (id,))
        cursor.execute("DELETE FROM dispositivo WHERE id_dispositivo=%s",(id,))
        conexion.connection.commit()
        cursor.close()
    
        
def obtener_ips(conexion):
        cursor=conexion.cursor()
        cursor.execute("SELECT id_dispositivo, mac_address, ip_actual FROM dispositivo")
        ip = cursor.fetchall()
        cursor.close()
        return ip

def actualizar_ip(conexion,id_dispositivo, nueva_ip):
        cursor=conexion.cursor()
        cursor.execute("UPDATE dispositivo SET ip_actual=%s WHERE id_dispositivo=%s", (nueva_ip, id_dispositivo))
        conexion.commit()
        cursor.close()

def insertar_metricas(conexion, id_dispositivo, fecha_ping, promedio, perdidos, disponible):
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO metricas (id_dispositivo_fk, fecha, latencia, paquetes_perdidos, disponibilidad)
        VALUES (%s, %s, %s, %s, %s)""", (id_dispositivo,fecha_ping, promedio, perdidos, disponible))
    conexion.commit()
    cursor.close()
    
def insertar_evento(conexion,id_dispositivo,alerta,descripcion,fecha):
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO evento (id_dispositivo_fk, tipo_alerta, descripcion, fecha)
        VALUES (%s, %s, %s, %s)
    """, (id_dispositivo,alerta,descripcion,fecha))
    conexion.commit()
    cursor.close()

def filtros(conexion, ubicacion):
    cursor = conexion.connection.cursor()
    if ubicacion==0:
        cursor.execute("""SELECT d.id_dispositivo, d.nombre_dispositivo,d.mac_address,d.ip_actual,t.tipo_dispositivo,u.ubicacion 
                    FROM dispositivo AS d
                    INNER JOIN tipo AS t
                    ON d.id_tipo_fk = t.id_tipo
                    INNER JOIN ubicacion AS u
                    ON d.id_ubicacion_fk = u.id_ubicacion
                    ORDER BY d.id_dispositivo ASC;""")
        dispositivos = cursor.fetchall()
        cursor.close()
        return dispositivos
    else: 
        cursor.execute("""SELECT d.id_dispositivo, d.nombre_dispositivo,d.mac_address,d.ip_actual,t.tipo_dispositivo,u.ubicacion 
                    FROM dispositivo AS d
                    INNER JOIN tipo AS t
                    ON d.id_tipo_fk = t.id_tipo
                    INNER JOIN ubicacion AS u
                    ON d.id_ubicacion_fk = u.id_ubicacion
                    WHERE id_ubicacion=%s
                    ORDER BY d.id_dispositivo ASC;""",(ubicacion,))
        dispositivos = cursor.fetchall()
        cursor.close()
        return dispositivos
    
def obtener_eventos(conexion, id_dispositivo):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT id_eveto, id_dispositivo_fk, tipo_alerta, descripcion, fecha
        FROM evento
        WHERE id_dispositivo_fk = %s
        ORDER BY id_eveto DESC
        LIMIT 4;
    """, (id_dispositivo,))
    eventos = cursor.fetchall()
    cursor.close()
    return eventos

def obtener_ultimos_eventos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT e.id_eveto, e.id_dispositivo_fk, e.tipo_alerta, e.descripcion, e.fecha, d.nombre_dispositivo
        FROM evento AS e
        INNER JOIN dispositivo AS d
        ON e.id_dispositivo_fk= d.id_dispositivo
        ORDER BY id_eveto DESC
        LIMIT 3;
    """)
    ultimos_eventos = cursor.fetchall()
    cursor.close()
    return ultimos_eventos

def obtener_dispositivos_criticos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT e.id_eveto,
        e.id_dispositivo_fk,d.nombre_dispositivo,d.mac_address,d.ip_actual,u.ubicacion,e.tipo_alerta,e.descripcion,e.fecha
        FROM evento AS e
        INNER JOIN dispositivo AS d
            ON e.id_dispositivo_fk = d.id_dispositivo
        INNER JOIN ubicacion AS u
            ON d.id_ubicacion_fk = u.id_ubicacion
        WHERE e.tipo_alerta = "Estado Crítico"
        ORDER BY e.id_eveto DESC;
    """)
    ultimos_eventos = cursor.fetchall()
    cursor.close()
    return ultimos_eventos

def eliminar_evento_db(conexion, id):
     cursor=conexion.connection.cursor()
     cursor.execute("DELETE FROM evento where id_eveto= %s", (id,))
     conexion.connection.commit()
     cursor.close()
    
def eliminar_eventos(conexion):
     cursor=conexion.connection.cursor()
     cursor.execute("DELETE FROM evento")
     conexion.connection.commit()
     cursor.close()
