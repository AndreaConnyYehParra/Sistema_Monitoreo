from database.db_utils import insertar_evento

def evaluar_metricas(conexion, id_dispositivo, fecha_ping, latencia, perdidos, disponible):
    
    #Convertir valor string a float o int
    try: latencia = float(latencia)
    except: latencia = None

    try: perdidos = int(perdidos)
    except: perdidos = 0

    try: disponible = int(disponible)
    except: disponible = 0


    if disponible == 0:
        alerta = "Estado Crítico"
        descripcion = "El dispositivo no responde (caída total)"
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → CRÍTICO por disponibilidad")
        return "critico"


    #Evaluación de latencia
    estado_latencia = "normal"

    if latencia is None:
        estado_latencia = "desconocido"

    elif latencia > 150:
        estado_latencia = "critico"

    elif 80 < latencia <= 150:
        estado_latencia = "advertencia"

    elif latencia <= 80:
        estado_latencia = "normal"


    #Evaluar perdida de paquetes
    estado_perdida = "normal"

    if perdidos == 4:
        estado_perdida = "critico"
    elif 1 <= perdidos <= 3:
        estado_perdida = "advertencia"
    elif perdidos == 0:
        estado_perdida = "normal"

     #Establece alertas

    if estado_latencia == "critico" or estado_perdida == "critico":
        estado_final = "critico"
        alerta = "Estado Crítico"
        descripcion = f"Posible congestión en la red. Latencia: {latencia} ms, Perdidas de paquetes: {perdidos}%"
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → CRÍTICO")
        return estado_final

    if estado_latencia == "advertencia" or estado_perdida == "advertencia":
        estado_final = "advertencia"
        alerta = "Advertencia"
        descripcion = f"Bajo rendimiento en la red. Latencia: {latencia} ms, Perdidas: {perdidos}%"
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → ADVERTENCIA")
        return estado_final

    # Si ninguna condicón se cumple, su estado es normal
    estado_final = "normal"
    alerta = "Estado Normal"
    descripcion = f"El dispositivo se encuentra estable en la red. Latencia: {latencia} ms, Perdidas: {perdidos}%"
    insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
    print("Evento → NORMAL")
    return estado_final