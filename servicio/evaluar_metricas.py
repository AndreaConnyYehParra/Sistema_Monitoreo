from database.db_utils import insertar_evento

def evaluar_latencia(latencia):
        try: latencia = float(latencia)
        except: 
            return "Crítico"
        
        if latencia <50:
            estado_latencia="Normal"
        elif  50<= latencia <=100:
            estado_latencia="Advertencia"
        else: 
            estado_latencia="Crítico"
        return estado_latencia 
        
def evaluar_paquetes(porcentaje):
        try: perdidos = int(porcentaje)
        except: 
            return "Crítico"
        
        # Casos críticos según los 4 pings
        if porcentaje == 25:
         return "Advertencia"
    
    # Caso saludable
        if porcentaje == 0:
         return "Normal"

    # Si llega algo inesperado, lo tratamos como crítico
        return "Crítico"
            
def evaluar_disponibilidad(disponible):
        try: disponible = int(disponible)
        except: 
            return "No disponible"
        
        if disponible == 1:
            estado_disponibilidad="Disponible"
        else: 
            estado_disponibilidad="No disponible"
        return estado_disponibilidad

def evaluar_metricas(conexion, id_dispositivo, fecha_ping, latencia,  porcentaje, disponible):

    latencia_estado=evaluar_latencia(latencia)
    paquetes_estado=evaluar_paquetes(porcentaje)
    disponibilidad_estado=evaluar_disponibilidad(disponible)
    
    #Prioridad 1: disponibilidad    
    if disponibilidad_estado == "No disponible":
        estado_final = "critico"
        alerta = "Estado Crítico"
        descripcion = f"El dispositivo no responde a las pruebas de conectividad."
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → NO DISPONIBLE")
        return estado_final
    
    #Prioridad 2: estado critico
    if  latencia_estado== "Crítico" or paquetes_estado == "Crítico": 
        estado_final = "critico"
        alerta = "Estado Crítico"
        descripcion = f"Condición crítica detectada en el dispositivo. Posible congestión, falla de red o indisponibilidad. Latencia: {latencia} ms, Perdidas de paquetes: {porcentaje}%"
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → CRÍTICO")
        return estado_final

    #Prioridad 3: estado advertencia
    elif  latencia_estado== "Advertencia" or paquetes_estado == "Advertencia":
        estado_final = "advertencia"
        alerta = "Advertencia"
        descripcion = f"El dispositivo se encuentra operativo, pero presenta bajo rendimiento en la red. Latencia: {latencia} ms, Perdidas: {porcentaje}%"
        insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
        print("Evento → ADVERTENCIA")
        return estado_final
    
    # Si ninguna condicón se cumple, su estado es normal
    else:
     estado_final = "normal"
     alerta = "Estado Normal"
     descripcion = f"El dispositivo se encuentra estable en la red. Latencia: {latencia} ms, Perdidas: {porcentaje}%"
     insertar_evento(conexion, id_dispositivo, alerta, descripcion, fecha_ping)
     print("Evento → NORMAL")
     return estado_final



        
        
        
    
