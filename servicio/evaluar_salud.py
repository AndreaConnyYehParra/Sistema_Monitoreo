from flask_mysqldb import MySQL
from database.config import Config

def evaluar_salud(total, criticos, advertencias, normales):
    
  # Normalizar valores None → 0
    total = total or 0
    criticos = criticos or 0
    advertencias = advertencias or 0
    normales = normales or 0

    # Si no hay dispositivos, evitar división entre cero
    if total == 0:
        return 0, 0, 0, 0, 0
    
    total_dispositivos = total
    dispositivos_criticos = criticos
    dispositivos_advertencias = advertencias
    dispositivos_normales = normales
    
    salud = (
        (normales * 1.0) +
        (advertencias * 0.5) +
        (criticos * 0.0)
    ) / total * 100

    salud = round(max(0, min(100, salud)), 1)
    
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
    
      # Si no hay dispositivos, evitar división entre cero
    if total is None or total == 0:
        return 0, 0

    # Si activos viene como None, convertirlo a 0
    if activos is None:
        activos = 0
    
    pct_disponibilidad = (activos / total) * 100 
    pct_nodisponibilidad = 100 - pct_disponibilidad

    return pct_disponibilidad, pct_nodisponibilidad


