from flask import *
import psycopg2
import os


app = Flask(__name__)


@app.route('/v1/health')
def create_api():

    name = os.environ.get('STUBA_MENO')         # nastavene system environment premenne
    passwrd = os.environ.get('STUBA_HESLO')

    conn_to_db = psycopg2.connect(              # pripajam sa do databazy
        host='147.175.150.216',
        port=5432,
        database='dota2',
        user=name,
        password=passwrd,
    )

    curs = conn_to_db.cursor()                  # vytvaram si kurzor na spracovavanie vratenych riadkov, pracu sa databazou
    curs.execute('SELECT VERSION();')

    version = curs.fetchall()[0][0]
    curs.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
    size = curs.fetchall()[0][0]

    data_dict = {                               # vytvaram si slovnik na vstupne data
        "pgsql":
            {
                'version': version,
                'dota2_db_size': size,
            }
    }

    conn_to_db.close()
    curs.close()
    return jsonify(data_dict)                   # data zo slovnika vraciam v .json formate


if __name__ == '__main__':                      # spustam aplikaciu
    app.run()
