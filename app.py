from flask import Flask #Importamos el framework Flask
from flask import render_template #Importamos el render para mostrar todos los templates
from flaskext.mysql import MySQL #Importamos para conectarnos a la BD

app = Flask(__name__) #Creamos la aplicación

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost' #Creamos la referencia al host, para que se conecte a la base de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_USER']='root' #Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_PASSWORD']='' #Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_BD']='sistema' #Nombre de nuestra BD

mysql.init_app(app) #Creamos la conexión con los datos

@app.route('/') #Hacemos el ruteo para que el usuario entre en la raiz

def index():
    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Juan Pablo', 'juanpablo@gmail.com', 'juanpablo.jpg');"
    conn = mysql.connect() #Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor() #Almacenaremos lo que ejecutamos
    cursor.execute(sql) #Ejecutamos la sentencia SQL
    conn.commit() #Cerramos la conexión
    
    return render_template('empleados/index.html') #Identifica la carpeta y el archivo html

if __name__=='__main__': #Estas lìneas de código las requiere python para que se pueda empezar a trabajar con la aplicación
    app.run(debug=True) #Corremos la aplicación en modo debug (con el código activamos el debugger)