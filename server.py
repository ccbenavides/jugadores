"""
en este modulo estoy haciendo peticiones http
con la ayuda de flask
"""
import os
import time
from flask import Flask, render_template, url_for, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

# Esta es la ruta donde descargara la imagen
app.config['UPLOAD_FOLDER'] = 'static/imagenes/'
# estas son las extension que estara aceptando
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
# recivira un file, retorno si tiene el tipo permitido
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# configuración de mysql con la aplicación
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'acuario203972'
app.config['MYSQL_DATABASE_DB'] = 'jugadores'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/', methods=['GET'])
def index():
    name = request.args.get("nombre") or ''
    cursor.execute('''select * from jugador where apodo like %s ''', name + "%")
    data = cursor.fetchall()
    return render_template('index.html', data=data, name=name)

@app.route('/admin')
def admin():
    name = request.args.get("nombre") or ''
    cursor.execute('''select * from jugador where apodo like %s ''', name + "%")
    data = cursor.fetchall()
    return render_template('admin.html', data=data, name=name)

@app.route('/view/<id_player>')
def view(id_player=None):
    cursor.execute(''' select * from jugador where idjugador=%s''', id_player)
    data = cursor.fetchone()
    cursor.execute(''' select estado, `name`  from vista_jugador
                        inner join vista on vista.idvista = vista_jugador.idvista
                        where idjugador = %s''', id_player)
    vistas = cursor.fetchall()
    return render_template('view.html', data=data, vistas=vistas)

@app.route('/create')
def create():
    return render_template('create.html')



@app.route('/edit_view/<id_player>')
def edit_view(id_player=None):
    # consulta que me resuelve la lista de todo lo que
    # puede visualizarse de un jugador especifico
    cursor.execute('''select descripcion, vista.idvista,estado from vista
                    inner join vista_jugador 
                    on vista.idvista = vista_jugador.idvista
                    where idjugador = %s;
                    ''', id_player)
    data = cursor.fetchall()
    longitud = len(data) - 1

    # consulta que me resulve un jugador expecifico
    # según su id
    cursor.execute(''' select idjugador, apodo from
                    jugador where idjugador=%s ''', id_player)
    jugador = cursor.fetchone()

    return render_template(
        'edit_view.html',
        data=data,
        jugador=jugador,
        longitud=longitud)

@app.route('/edit_permisos/<int:post_id>', methods=['POST'])
def show_post(post_id):
    # !mover los rangos según como estan los id de <vista> en la base de datos
    for a in range(int(request.form['id_vista_first'])
                   , int(request.form['id_vista_last']) + 1):
        cursor.execute(""" UPDATE vista_jugador SET estado = %s
                    WHERE idjugador = %s and idvista = %s """,
                       (request.form[str(a)], post_id, a))

    return redirect(url_for('admin'))


@app.route('/crear_jugador', methods=['POST'])
def crear_jugador():
    file_player = request.files['file']
    if file_player.filename != '':
        ext = file_player.filename.rsplit('.', 1)[1]
        nombre_imagen = str(round(time.time() * 1000)) + "." + str(ext)
    else:
        ext = ''
        nombre_imagen = ''

    #change = request.args.get('premio', None)
    cursor.execute("""insert into jugador
                    (`apodo`, `nombre`, `mundiales`, `copas`, `goles`, `historia`, `url_img`,`premios`) 
                    values 
                    (%s, %s, %s, %s, %s, %s , %s, %s);
                """, (request.form['apodo']
                      , request.form['nombre']
                      , request.form['mundiales']
                      , request.form['copas']
                      , request.form['goles']
                      , request.form['historia']
                      , nombre_imagen
                      , request.form['premios']))

    cursor.execute("""insert into vista_jugador  (`idvista`, `idjugador`)
                    select idvista,LAST_INSERT_ID() from vista;""")

    cursor.execute(""" SELECT LAST_INSERT_ID() """)
    jugador_id = cursor.fetchone()
    conn.commit()

    # si el file esta vacio no guarda imagen y te redirecciona a la vista admin
    if file_player.filename == '':
        redirect(url_for('admin'))

    if file_player and allowed_file(file_player.filename):

        file_player.save(
            os.path.join(app.config['UPLOAD_FOLDER']
                         , nombre_imagen))

    return redirect(url_for('admin'))



# aca al ultimo agrega esto
@app.route('/edit/<id_player>')
def edit(id_player=None):
    cursor.execute(''' select * from jugador where idjugador=%s''', id_player)
    data = cursor.fetchone()
    return render_template('edit.html', data=data)




@app.route('/actualizar/<id_player>', methods=['POST'])
def actualizar(id_player=None):
    file_player = request.files['file']
    if file_player.filename != '':
        ext = file_player.filename.rsplit('.', 1)[1]
        nombre_imagen = str(round(time.time() * 1000)) + "." + str(ext)
    else:
        ext = ''
        nombre_imagen = request.form['imagen']

    cursor.execute('''UPDATE jugador SET
apodo = %s,
nombre = %s,
mundiales = %s,
copas = %s,
goles = %s,
historia = %s,
url_img = %s,
premios = %s
WHERE idjugador = %s;
    ''', (request.form['apodo']
          , request.form['nombre']
          , request.form['mundiales']
          , request.form['copas']
          , request.form['goles']
          , request.form['historia']
          , nombre_imagen
          , request.form['premios']
          , id_player))
    conn.commit()
    # si el file esta vacio no guarda imagen y te redirecciona a la vista admin
    if file_player.filename == '':
        redirect(url_for('admin'))

    if file_player and allowed_file(file_player.filename):
        file_player.save(
            os.path.join(app.config['UPLOAD_FOLDER']
                         , nombre_imagen))

    return redirect(url_for('admin'))




@app.route('/delete/<id_player>', methods=['GET'])
def delete(id_player=None):
    cursor.execute('delete from vista_jugador where idjugador=%s', id_player)
    conn.commit()
    cursor.execute('delete from jugador where idjugador=%s', id_player)
    conn.commit()
    return redirect(url_for('admin'))
