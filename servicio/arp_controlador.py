import subprocess

def obtener_tabla_arp():
    #Comando para obtener la tabla arp de las ips conocidas
    comando_arp=["arp", "-a"]
    
    try:
        resultado = subprocess.run(
            comando_arp, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
        
        texto = resultado.stdout.decode("cp850", errors="ignore")
        
        #lista para guardar los datos de la tabla
        tabla = []

        for linea in texto.splitlines():
            if "-" in linea and "." in linea:
                partes = linea.split()
                ip = partes[0]
                mac = partes[1]
                #Almacenar los valores de ip y mac como diccionario
                tabla.append({"ip": ip, "mac": mac})
                
        return tabla
    
    except Exception as e:
        print("Error:", e)
        return False

def normalizar_mac(mac):
    # Quita guiones y dos puntos, convierte a minúsculas
    return mac.replace("-", "").replace(":", "").lower()

def buscar_ip(tabla, mac_buscada):
    try:
        mac_normalizada=normalizar_mac(mac_buscada)
        for dispositivo in tabla:
            mac_tabla_normalizada = normalizar_mac(dispositivo["mac"])
            if mac_tabla_normalizada == mac_normalizada:
                return dispositivo["ip"]
            
        return None
    except Exception as e:
        print("Error:", e)
        return None