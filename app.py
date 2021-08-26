from flask import Flask #Importamos el framework Flask
from flask import render_template,request,redirect #Importamos el render para mostrar todos los templates
from flaskext.mysql import MySQL #Importamos para conectarnos a la BD
from datetime import datetime #Nos permitirá darle el nombre a la foto

app = Flask(__name__) #Creamos la aplicación

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost' #Creamos la referencia al host, para que se conecte a la base de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_USER']='root' #Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_PASSWORD']='' #Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_BD']='sistema' #Nombre de nuestra BD

mysql.init_app(app) #Creamos la conexión con los datos


@app.route('/') #Hacemos el ruteo para que el usuario entre en la raiz
def index():
    sql = "SELECT * FROM `sistema`.`empleados`;"
    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    cursor.execute(sql) #Ejecutamos la sentencia SQL
    empleados=cursor.fetchall() #Traemos toda la información
    print(empleados) #Imprimimos los datos en la terminal
    conn.commit() #Cerramos la conexión  
    return render_template('empleados/index.html', empleados=empleados) #Identifica la carpeta y el archivo htm

@app.route('/destroy/<int:id>') #Recibe como parámetro el id del registro
def destroy(id):
    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id)) #En vez de pasarle el string la escribimos
    conn.commit() #Cerramos la conexión
    return redirect('/') #Regresamos de donde vinimos
    
@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    now = datetime.now() #Para añadir al nombre del archivo subido
    tiempo = now.strftime("%Y%H%M%S") #Años horas minutos y segundos
    
    if _foto.filename!='':
        nuevoNombreFoto = tiempo + _foto.filename #Concatena el nombre
        _foto.save('uploads/'+nuevoNombreFoto) #Lo guarda en la carpeta 'uploads'

    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,_correo, nuevoNombreFoto)

    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    cursor.execute(sql,datos) #Ejecutamos la sentencia SQL
    conn.commit() #Cerramos la conexión
    return render_template('empleados/index.html') #Identifica la carpeta y el archivo html

if __name__=='__main__': #Estas lìneas de código las requiere python para que se pueda empezar a trabajar con la aplicación
    app.run(debug=True) #Corremos la aplicación en modo debug (con el código activamos el debugger)