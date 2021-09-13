from flask import Flask  # Importamos el framework Flask
# Importamos el render para mostrar todos los templates
from flask import render_template, request, redirect, url_for,flash
from flask import send_from_directory #Acceso a las UPLOAD_FOLDERs
from flask_sqlalchemy import SQLAlchemy  # Importamos para conectarnos a la BD
from datetime import datetime  # Nos permitirá darle el nombre a la foto
import os  # Nos pemite acceder a los archivos
from werkzeug.utils import secure_filename
from models import db, Employee


app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://erfuhkjhwvckgq@localhost/dante-crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(16)

# Configs for uploading photos
UPLOAD_FOLDER = os.path.join('data/uploads') 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/data/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/data/no-photo.svg')
def noPhoto():
    return send_from_directory( os.path.join('data'), 'no-photo.svg')

@app.route('/')
def index():
    employees = Employee.query.order_by(Employee.id).all() # Gets all the values from Employee table, sorted by ID
    employeesCount = Employee.query.count() # Counts the values

    return render_template('/employee/index.html', employees=employees, employeesCount=employeesCount)


@app.route('/destroy/<int:deleteID>')
def destroy(deleteID):
    #Gets the employee that matches the ID
    toDelete = Employee.query.filter_by(id = deleteID).first_or_404()

    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], toDelete.photo)) # Removes file from path
    except:
        pass
    
    db.session.delete(toDelete) #Updates DB

    db.session.commit()

    return redirect('/') 


@app.route('/edit/<int:editID>')
def edit(editID):
    #Gets the employee that matches the ID
    toEdit = Employee.query.filter_by(id = editID).first_or_404()

    db.session.commit()
    return render_template('employee/edit.html', employee=toEdit)


@app.route('/update/<int:updateID>', methods=['POST'])
def update(updateID):
    #Request data from form
    _name = request.form['nameInput']
    _surname = request.form['surnameInput']
    _mail = request.form['mailInput']
    _photo = request.files['photoInput']

    #Gets the employee that matches the ID
    toUpdate = Employee.query.filter_by(id = updateID).first_or_404()

    #Updates DB
    toUpdate.name = _name
    toUpdate.surname = _surname
    toUpdate.mail = _mail

    #Changes the photo only if it has been modified
    if _photo:
        if allowed_file(_photo.filename):
            try:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            except FileExistsError:
                pass #Fails silently when there's already a folder named 'uploads' 

            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], toUpdate.photo)) #Removes file from path
            except:
                pass 
            
            #Gets the time for the new filename
            now = datetime.now()
            date = now.strftime("%Y%H%M%S")

            filename = secure_filename(date+_photo.filename)
            _photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #Saves the new file into path
            
            toUpdate.photo = filename # Updates DB
        else:
            flash('Formato de imagen no válido') #Alert when use tries to upload a not allowed file 
            return  redirect('/edit/'+str(updateID))

    db.session.commit()

    return redirect('/')

@app.route('/delete-pp/<int:deleteID>')
def deletePP(deleteID):
    #Gets the employee that matches the ID
    cursor = Employee.query.filter_by(id = deleteID).first_or_404()
        
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], cursor.photo)) #Removes file from path
    except FileNotFoundError:
        pass 
    
    cursor.photo = None #Updates DB
    db.session.commit()

    return redirect('/')

@app.route('/create')
def create():
    return render_template('employee/create.html')


@app.route('/store', methods=['POST'])
def storage():
    #Request data from form
    _name = request.form['nameInput']
    _surname = request.form['surnameInput']
    _mail = request.form['mailInput']
    _photo = request.files['photoInput']

    #Checks data
    if _name == '' or _surname == '' or _mail == '':
        flash('Recuerda llenar los datos de los campos') #Sends msg
        return redirect(url_for('create'))

    #Gets the time for the new filename
    now = datetime.now()  
    date = now.strftime("%Y%H%M%S")
    
    try:
        os.mkdir(app.config['UPLOAD_FOLDER'])
    except FileExistsError:
        pass # Fails silently when there's already a folder named 'uploads' 

    filename = None # If not mofified, Employee gets None (null) image

    if _photo:
        if allowed_file(_photo.filename):
            filename = secure_filename(date+_photo.filename)
            _photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Saves new file into path
        else:
            flash('Formato de imagen no válido') # Alert when use tries to upload a not allowed file 
            return redirect(url_for('create')) 
        
    entry = Employee(_name, _surname, _mail, filename) # Generates a new Employee. 
    db.session.add(entry) # Adds the new Employee into the DB

    db.session.commit()

    return redirect('/')

if __name__ == '__main__': 
    db.init_app(app)
    db.create_all() 
    app.run(port=3000, debug=True)
