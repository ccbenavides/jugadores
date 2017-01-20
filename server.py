"""
en este modulo estoy haciendo peticiones http
con la ayuda de flask
"""
from flask import Flask, render_template, url_for, request, redirect
from flaskext.mysql import MySQL
import json

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

    return render_template('view.html', data)

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
    array_jugadores = str(request.get_data())
    #change = request.args.get('premio', None)
    cursor.execute("""insert into jugador
                    (`apodo`, `nombre`, `mundiales`, `copas`, `goles`, `historia`, `url_img`) 
                    values 
                    (%s, %s, %s, %s, %s, %s , %s);
                """, (request.form['apodo']
                      , request.form['nombre']
                      , request.form['mundiales']
                      , request.form['copas']
                      , request.form['goles']
                      , request.form['historia']
                      , ""))

    cursor.execute("""insert into vista_jugador  (`idvista`, `idjugador`)
                    select idvista,LAST_INSERT_ID() from vista;""")

    cursor.execute(""" SELECT LAST_INSERT_ID() """)
    jugador_id = cursor.fetchone()
    # payload = json.loads(request.get_data().decode('utf-8'))

    for array in array_jugadores.split("&"):
        if array.split("=")[0] == "premio_":
            cursor.execute(""" insert into premios (descripcion, idjugador )
                        values ( %s, %s)""",
                           (array.split("=")[1], jugador_id[0]))
    conn.commit()

    # conn.commit()
    # return array_jugadores
    return redirect(url_for('admin'))

# aca al ultimo agrega esto
@app.route('/edit/<id_player>')
def edit(id_player=None):
    cursor.execute(''' select * from jugador where idjugador=%s''', id_player)
    data = cursor.fetchone()
    return render_template('edit.html', data=data)

@app.route('/actualizar/<id_player>', methods=['POST'])
def actualizar(id_player=None):
    cursor.execute('''UPDATE jugador SET
apodo = %s,
nombre = %s,
mundiales = %s,
copas = %s,
goles = %s,
historia = %s,
url_img = %s
WHERE idjugador = %s;
    ''', (request.form['apodo']
          , request.form['nombre']
          , request.form['mundiales']
          , request.form['copas']
          , request.form['goles']
          , request.form['historia']
          , ""
          , id_player))
    conn.commit()
    return redirect(url_for('admin'))


@app.route('/delete/<id_player>', methods=['GET'])
def delete(id_player=None):
    cursor.execute('delete from premios where idjugador=%s', id_player)
    conn.commit()
    cursor.execute('delete from vista_jugador where idjugador=%s', id_player)
    conn.commit()
    cursor.execute('delete from jugador where idjugador=%s', id_player)
    conn.commit()
    return redirect(url_for('admin'))
