from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_mysqldb import MySQL, MySQLdb

from flask_login import LoginManager,UserMixin
import flask_login
import bcrypt
import hashlib


app = Flask(__name__)
login = LoginManager(app)
app.secret_key = 'many random bytes'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'passer'
app.config['MYSQL_DB'] = 'gestion_logement'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/page_admin')
def lister_user():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, prenom, nom, email, username, fonction, Pavillon_nom_pavillon, numero FROM gestionnaire where etat='activer'")
	rows = cur.fetchall()
	cur.close()
	return render_template('pages_admin/index.html', users = rows)


# Ajout d'utilisateur
@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':

        numero = request.form['numero']
        nom = request.form['nom']
 
        prenom = request.form['prenom']

        mdp = request.form['password'].encode("utf-8")

        fonction = request.form['fonction']
        username = request.form['username']
        pavillon = request.form['pavillon']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO gestionnaire(nom,prenom,mdp,fonction,etat,email,username,pavillon_nom_pavillon, numero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nom, prenom, mdp, fonction, "Activer", email, username, pavillon, numero))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('lister_user'))


# Suppression
@app.route('/user/<string:user_id>/delete', methods = ['POST'])
def delete(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
    UPDATE gestionnaire
    SET etat = "Desactiver"
    WHERE id = %s
    """, user_id)
    mysql.connection.commit()
    #cur.close()
    return redirect(url_for('lister_user'))


# Modification
@app.route('/<string:user_id>/update',methods = ['POST'])
def update(user_id):
    if request.method == 'POST':

        # id = request.form['id']
        nom = request.form['nom']

        prenom = request.form['prenom']

        fonction = request.form['fonction']

        pavillon = request.form['pavillon']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE gestionnaire
        SET nom = %s, prenom = %s, fonction = %s, pavillon_nom_pavillon = %s
        WHERE id = %s
        """, (nom,prenom,fonction,pavillon, user_id))
        flash('Data Updtated Successfully')
        mysql.connection.commit()
        #cur.close()
        return redirect(url_for('lister_user'))



# Login Manager

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login/home.html')


@login_manager.user_loader
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login/login.html")
    if request.method == "POST":
        
        details = request.form
        identifiant =  request.form['identifiant']
        mdp = details['mdp'].encode("utf-8")
        pw_hash = bcrypt.hashpw(mdp,bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        
        #cur.execute("INSERT INTO administrateur(prenom,nom,login, mdp) VALUES (%s,%s, %s, %s)", (prenom,nom,identifiant,pw_hash))
        cur.execute("SELECT * FROM administrateur WHERE login =%s or username=%s",(identifiant,identifiant,))
        user = cur.fetchone()
        cur.close()
        p=hashlib.sha256(mdp).hexdigest()
       
        
        if user != None:
            if p == user["mdp"]:
                session['identifiant']=user["username"]
                session['prenom']=user["prenom"]
                return redirect(url_for('lister_user'))
            else:
                 return render_template('login/mot_passe_incorrecte.html')
        else:
            return render_template('login/mot_passe_incorrecte.html')


            
@app.route('/register', methods=['GET', 'POST'])
def registerAdmin():
    if request.method == "GET":
        return render_template("login/register.html")
    else:
        details = request.form
        identifiant = details['email']
        mdp = details['mdp'].encode("utf-8")
        prenom = details['prenom']
        nom = details['nom']
        username = details['username']
        salt=bcrypt.gensalt()

        pw_hash =hashlib.sha256(mdp).hexdigest()

        #hash_password=bcrypt.hashpw(mdp,bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO administrateur(prenom,nom,login,mdp,username) VALUES (%s,%s, %s,%s,%s)", (prenom,nom,identifiant,pw_hash,username))
        mysql.connection.commit()
        session['prenom'] = prenom
        session['nom'] = nom
        session['identifiant'] = identifiant
        
        cur.close()
        return redirect(url_for('home'))
    return render_template('login/login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

 

if __name__ == '__main__':
    app.run(debug = True)