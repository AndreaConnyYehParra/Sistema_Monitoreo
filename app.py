from flask import Flask, render_template, request, jsonify, redirect, flash, session
from flask_mysqldb import MySQL
from database.config import Config
from  database.db_utils import obtener_tipos, obtener_ubicaciones, obtener_dispositivos, insertar_dispositivo, actualizar_dispositivo, eliminar_dispositivo, obtener_dispositivos_card, filtros, obtener_eventos, obtener_ultimos_eventos, obtener_dispositivos_criticos, eliminar_evento_db, eliminar_eventos
app=Flask(__name__)

app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB

conexion = MySQL(app)
app.secret_key = "890HJK"


@app.route('/')
def index():
    
    return render_template('index.html') 

@app.route('/admin/dispositivos')
def AdminDispositivos():
    ubicacion = request.args.get('ubicacion', default=0, type=int)
    tipos= obtener_tipos(conexion)
    ubicaciones= obtener_ubicaciones(conexion)
    dispositivos= filtros(conexion, ubicacion) 
    ultimos_eventos=obtener_ultimos_eventos(conexion)
    return render_template('admin-dispositivos.html', tipos=tipos, ubicaciones=ubicaciones, dispositivos=dispositivos, ubicacion=ubicacion, ueventos=ultimos_eventos)
    
    

@app.route('/monitoreo/dispositivos')
def MonitoreoDispositivos():
    ubicacion = request.args.get('ubicacion', default=0, type=int)
    ubicaciones= obtener_ubicaciones(conexion)
    dispositivos= obtener_dispositivos_card(conexion, ubicacion) 
    ultimos_eventos=obtener_ultimos_eventos(conexion)
    eventos = {}
    for d in dispositivos:
        eventos[d[1]] = obtener_eventos(conexion, d[1])
        
    return render_template('monitoreo-dispositivos.html', ubicaciones=ubicaciones, dispositivos=dispositivos, ubicacion=ubicacion, eventos=eventos, ueventos=ultimos_eventos)
    

@app.route('/eventos/dispositivos')
def EventosDispositivos():
    
    return render_template('eventos-dispositivos.html')

@app.route('/criticos/dispositivos')
def CriticosDispositivos():
    dispositivos= obtener_dispositivos_criticos(conexion) 
    ultimos_eventos=obtener_dispositivos_criticos(conexion)
    return render_template('criticos-dispositivos.html', dispositivos=dispositivos, ueventos=ultimos_eventos)

@app.route('/agregar-dispositivo', methods=['POST'])
def storage():
    
    _nombre=request.form['nombre']
    _macadd=request.form['macadd']
    _ip_actual=request.form['ip']
    _tipo=request.form['tipo']
    _ubicacion=request.form['ubicacion']
        
    try: 
        insertar_dispositivo(conexion, _nombre, _macadd, _ip_actual, _tipo, _ubicacion)
        flash("Dispositivo agregado correctamente", "success")
        return redirect('/admin/dispositivos')
    except Exception as ex:
        flash("Error al agregar el dispositivo", "danger")
        return redirect('/admin/dispositivos')
    
@app.route('/editar/dispositivo', methods=['POST'])
def editar():       
    _nombre=request.form['nombre']
    _macadd=request.form['macadd']
    _ip_actual=request.form['ip']
    _tipo=request.form['tipo']
    _ubicacion=request.form['ubicacion']
    _id=request.form['id']
        
    try: 
        actualizar_dispositivo(conexion, _nombre, _macadd, _ip_actual, _tipo, _ubicacion,_id)
        flash("Dispositivo Editado Correctamente", "primary")
        return redirect('/admin/dispositivos')
    except Exception as ex:
        flash("Error al editar el dispositivo", "danger")
        return redirect('/admin/dispositivos')
    
    
@app.route('/eliminar/<int:id>')
def eliminar(id):       
    try: 
        eliminar_dispositivo(conexion,  id)
        flash("Dispositivo Eliminado Correctamente", "info")
        return redirect('/admin/dispositivos')
    except Exception as ex:
        flash("Error al eliminar el dispositivo", "danger")
        return redirect('/admin/dispositivos')

@app.route('/eliminar/evento/<int:id>')
def eliminar_evento_route(id):       
    try: 
        eliminar_evento_db(conexion,  id)
        flash("Evento Eliminado Correctamente", "info")
        return redirect('/criticos/dispositivos')
    except Exception as ex:
        flash("Error al eliminar el evento", "danger")
        return redirect('/criticos/dispositivos')
    
@app.route('/eliminar/eventos')
def eliminar_eventos_route():       
    try: 
        eliminar_eventos(conexion)
        flash("Eventos Eliminado Correctamente", "info")
        return redirect('/criticos/dispositivos')
    except Exception as ex:
        flash("Error al eliminar eventos", "danger")
        return redirect('/criticos/dispositivos')

if __name__=='__main__':
    app.run(debug=True)
    
    