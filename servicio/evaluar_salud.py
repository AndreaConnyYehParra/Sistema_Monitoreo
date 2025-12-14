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
    
    if salud >= 90:
        estado = "Saludable"
    elif salud >= 70:
        estado = "Degradada"
    else:
        estado = "Critico"

    return round(salud), estado