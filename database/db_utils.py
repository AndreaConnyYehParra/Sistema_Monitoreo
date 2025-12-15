
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
        cursor.execute("DELETE FROM evento WHERE id_dispositivo_fk=%s",(id,))
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

def obtener_todos_eventos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT e.id_eveto,e.id_dispositivo_fk,d.nombre_dispositivo,d.mac_address,d.ip_actual,u.ubicacion,e.tipo_alerta,e.descripcion,e.fecha
        FROM evento AS e
        INNER JOIN dispositivo AS d
            ON e.id_dispositivo_fk = d.id_dispositivo
        INNER JOIN ubicacion AS u
            ON d.id_ubicacion_fk = u.id_ubicacion
        ORDER BY e.id_eveto DESC;
    """)
    todos_eventos = cursor.fetchall()
    cursor.close()
    return todos_eventos

def obtener_disponibilidad(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
    SELECT 
    SUM(CASE WHEN m.disponibilidad = 1 THEN 1 ELSE 0 END) AS disponibles,
    SUM(CASE WHEN m.disponibilidad = 0 THEN 1 ELSE 0 END) AS no_disponibles
    FROM metricas AS m
    WHERE m.fecha = (
    SELECT MAX(m2.fecha)
    FROM metricas AS m2
    WHERE m2.id_dispositivo_fk = m.id_dispositivo_fk
    );
    """)
    disponibilidad = cursor.fetchone()
    activos, inactivos = disponibilidad
    cursor.close()
    return activos, inactivos

def obtener_umonitoreo(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
    SELECT MAX(fecha) AS ultima_monitoreo
    FROM metricas;
    """)
    ultimo_monitoreo = cursor.fetchone()
    cursor.close()
    return ultimo_monitoreo[0]

def obtener_deventos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
        SELECT e.id_eveto, e.id_dispositivo_fk, e.tipo_alerta, e.descripcion, e.fecha, d.nombre_dispositivo
        FROM evento AS e
        INNER JOIN dispositivo AS d
        ON e.id_dispositivo_fk= d.id_dispositivo
        ORDER BY id_eveto DESC
        LIMIT 6;
    """)
    ultimos_deventos = cursor.fetchall()
    cursor.close()
    return ultimos_deventos

def obtener_ndispositivos(conexion):
     cursor = conexion.connection.cursor()
     cursor.execute("""
        SELECT COUNT(*) AS total_dispositivos
        FROM dispositivo;
        """)
     resultado = cursor.fetchone()
     cursor.close()
     return  resultado[0]
            
            
def obtener_disnormal(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) AS normal
    FROM (
        SELECT e.tipo_alerta
        FROM evento e
        INNER JOIN (
            SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
            FROM evento
            GROUP BY id_dispositivo_fk
        ) ult
        ON e.id_dispositivo_fk = ult.id_dispositivo_fk
        AND e.fecha = ult.ultima_fecha
    ) AS ultimos
    WHERE tipo_alerta = 'Estado Normal';
    """)
    dis_normal = cursor.fetchone()
    cursor.close()
    return dis_normal[0]

def obtener_discriticos(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) AS criticos
    FROM (
        SELECT e.tipo_alerta
        FROM evento e
        INNER JOIN (
            SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
            FROM evento
            GROUP BY id_dispositivo_fk
        ) ult
        ON e.id_dispositivo_fk = ult.id_dispositivo_fk
        AND e.fecha = ult.ultima_fecha
    ) AS ultimos
    WHERE tipo_alerta = 'Estado Crítico';
    """)
    dis_criticos = cursor.fetchone()
    cursor.close()
    return dis_criticos[0]

def obtener_disadvertencia(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
    SELECT COUNT(*) AS advertencia
    FROM (
        SELECT e.tipo_alerta
        FROM evento e
        INNER JOIN (
            SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
            FROM evento
            GROUP BY id_dispositivo_fk
        ) ult
        ON e.id_dispositivo_fk = ult.id_dispositivo_fk
        AND e.fecha = ult.ultima_fecha
    ) AS ultimos
    WHERE tipo_alerta = 'Advertencia';
    """)
    dis_advertencia = cursor.fetchone()
    cursor.close()
    return dis_advertencia[0]

def obtener_promedios(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
                SELECT 
                t.tipo_dispositivo AS tipo,
                AVG(m.latencia) AS latencia_promedio,
                AVG(m.paquetes_perdidos) AS perdida_promedio
            FROM (
                SELECT m.*
                FROM metricas m
                INNER JOIN (
                    SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
                    FROM metricas
                    GROUP BY id_dispositivo_fk
                ) ult
                    ON m.id_dispositivo_fk = ult.id_dispositivo_fk
                    AND m.fecha = ult.ultima_fecha
            ) m
            INNER JOIN dispositivo d
                ON m.id_dispositivo_fk = d.id_dispositivo
            INNER JOIN tipo t
                ON d.id_tipo_fk = t.id_tipo
            GROUP BY t.tipo_dispositivo;
    """)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados  

def obtener_top_latencia(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
                SELECT 
                    d.nombre_dispositivo AS dispositivo,
                    t.tipo_dispositivo AS tipo,
                    m.latencia
                FROM (
                    SELECT m.*
                    FROM metricas m
                    INNER JOIN (
                        SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
                        FROM metricas
                        GROUP BY id_dispositivo_fk
                    ) ult
                        ON m.id_dispositivo_fk = ult.id_dispositivo_fk
                        AND m.fecha = ult.ultima_fecha
                ) m
                INNER JOIN dispositivo d
                    ON m.id_dispositivo_fk = d.id_dispositivo
                INNER JOIN tipo t
                    ON d.id_tipo_fk = t.id_tipo
                ORDER BY m.latencia DESC
                LIMIT 5;
    """)
    top_latencia = cursor.fetchall()
    cursor.close()
    return top_latencia

def obtener_top_perdidas(conexion):
    cursor = conexion.connection.cursor()
    cursor.execute("""
                SELECT 
                    d.nombre_dispositivo AS dispositivo,
                    t.tipo_dispositivo AS tipo,
                    m.paquetes_perdidos
                FROM (
                    SELECT m.*
                    FROM metricas m
                    INNER JOIN (
                        SELECT id_dispositivo_fk, MAX(fecha) AS ultima_fecha
                        FROM metricas
                        GROUP BY id_dispositivo_fk
                    ) ult
                        ON m.id_dispositivo_fk = ult.id_dispositivo_fk
                        AND m.fecha = ult.ultima_fecha
                ) m
                INNER JOIN dispositivo d
                    ON m.id_dispositivo_fk = d.id_dispositivo
                INNER JOIN tipo t
                    ON d.id_tipo_fk = t.id_tipo
                ORDER BY m.paquetes_perdidos DESC
                LIMIT 5;
    """)
    top_perdidas = cursor.fetchall()
    cursor.close()
    return top_perdidas  
 
 
 

 
