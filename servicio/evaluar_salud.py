from flask_mysqldb import MySQL
from database.config import Config

def evaluar_salud(total, criticos, advertencias, normales):
    total_dispositivos = total
    dispositivos_criticos = criticos
    dispositivos_advertencias = advertencias
    dispositivos_normales = normales
    
    salud = (
        (dispositivos_normales * 100) +
        (dispositivos_advertencias * 50) +
        (dispositivos_criticos * 0)
    )/ (total_dispositivos)
    
    pct_criticos = (dispositivos_criticos / total_dispositivos) * 100
    pct_advertencias = (dispositivos_advertencias / total_dispositivos) * 100
    pct_normales = (dispositivos_normales / total_dispositivos) * 100
    
    if salud >= 90:
        estado = "Saludable"
    elif salud >= 70:
        estado = "Degradada"
    else:
        estado = "Critico"

    return round(salud), estado, round(pct_criticos, 1), round(pct_advertencias, 1), round(pct_normales, 1)

def evaluar_disponibilidad(total, dispositivos_activos):
    total= total
    activos= dispositivos_activos 
    
    pct_disponibilidad = (activos / total) * 100 
    pct_nodisponibilidad = 100 - pct_disponibilidad

    return pct_disponibilidad, pct_nodisponibilidad


