from flask import Flask, render_template, request, redirect, url_for, flash

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'passer'
app.config['MYSQL_DB'] = 'gestion_logement'

mysql = MySQL(app)

@app.route('/')

def home():
    return render_template('liste_etudiants.html')

@app.route('/lister')

def new_student():
    return render_template('listerReservation.html')

    #Valider reservation
@app.route('/',methods = ['POST', 'GET'])

def ValiderReservation():

    if request.method == "POST":

        identifiant =  request.form['identifiant']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE reservation
        SET etat_payement = "payer", Gestionnaire_id = identifiant
        WHERE Etudiant_id = %s
        """)
        mysql.connection.commit()
        #cur.close()
        return render_template('listReservation.html')


#Liste reservation
@app.route('/lister')

def listReservation():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id,Etudiant_id,date_payement,etat_payement,date_reservation,Gestionnaire_id FROM reservation")
    rows = cur.fetchall()
    cur.close()
    return render_template('listerReservation.html', reservation=rows)



if __name__ == '__main__':
    app.run(debug = True)
