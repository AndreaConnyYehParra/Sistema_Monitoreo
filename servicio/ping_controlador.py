import subprocess
from datetime import datetime 

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
        fecha_ping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enviados = recibidos = perdidos = 0
        minimo = maximo = promedio = 0
        disponible = 0

        # Analizar líneas del ping
        for linea in salida.splitlines():

            # Paquetes:
            if "Paquetes" in linea:
                paquetes = linea.replace("Paquetes: ", "").split(",")
                if len(paquetes) >= 3:
                    enviados = int(paquetes[0].split("=")[1].strip())
                    recibidos = int(paquetes[1].split("=")[1].strip())
                    perdidos = int(paquetes[2].split("=")[1].strip())
                    porcentaje=(perdidos/enviados)*100
                    
            # Tiempos:
            if "Mínimo" in linea:
                latencia = linea.replace("ms", "").split(",")
                if len(latencia) >= 3:
                   minimo = latencia[0].split("=")[1].strip()
                   maximo = latencia[1].split("=")[1].strip()
                   promedio = latencia[2].split("=")[1].strip()
                   
            fecha_ping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        print(f"\nIP: {ip}")
        print(f"Paquetes → Enviados: {enviados} | Recibidos: {recibidos}| Perdidos: {perdidos} | porcentaje {porcentaje} ")
        print(f"Latencia → Min: {minimo} ms | Max: {maximo} ms | Promedio: {promedio} ms")

        disponible = 1 if resultado.returncode == 0 else 0

        return (fecha_ping, minimo, maximo, promedio, perdidos, disponible, enviados, recibidos, porcentaje)

    except Exception as e:
        print("Error:", e)
        return (fecha_ping, 0, 0, 0, 0, 0, 0, 0)