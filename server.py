"""
en este modulo estoy haciendo peticiones http
con la ayuda de flask
"""
from flask import Flask, render_template, url_for, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

# configuración de mysql con la aplicación
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'acuario203972'
app.config['MYSQL_DATABASE_DB'] = 'jugadores'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    cursor.execute('''select * from jugador''')
    data = cursor.fetchall()
    return render_template('admin.html', data=data)

@app.route('/view/<id_player>')
def view(id_player=None):
    return render_template('view.html', id_player=id_player)

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

    # consulta que me resulve un jugador expecifico
    # según su id
    cursor.execute(''' select idjugador, apodo from
                    jugador where idjugador=%s ''', id_player)
    jugador = cursor.fetchone()

    return render_template('edit_view.html', data=data, jugador=jugador)

@app.route('/edit_permisos/<int:post_id>', methods=['POST'])
def show_post(post_id):
    # !mover los rangos según como estan los id de <vista> en la base de datos
    for a in range(10, 15):
        cursor.execute(""" UPDATE vista_jugador SET estado = %s
                    WHERE idjugador = %s and idvista = %s """,
                       (request.form[str(a)], post_id, a))

    return redirect(url_for('admin'))


@app.route('/crear_jugador', methods=['POST'])
def crear_jugador():
    return request.form["premio[]"]
    #return redirect(url_for('admin'))
    