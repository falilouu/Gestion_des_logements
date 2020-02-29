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
    return render_template('index.html')

@app.route('/entrernouveau')

def new_gestionnaire():
    return render_template('result.html')



@app.route('/update',methods = ['POST', 'GET'])

def updateGestionnaire():
    if request.method == 'POST':

            id = request.form['id']

	    username = request.form['username']
		
	
            mdp = request.form['password'].encode("utf-8")

            

            cur = mysql.connection.cursor()

            cur.execute("""
            UPDATE gestionnaire
            SET mdp = %s, username = %s
            WHERE id = %s
            """, (mdp,username))

            flash('Data Updtated Successfully')

            mysql.connection.commit()
            #cur.close()
            return redirect(url_for('Index'))




if __name__ == '__main__':
    app.run(debug = True)
