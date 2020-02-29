from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_mysqldb import MySQL, MySQLdb

from flask_mail import Mail , Message

#pour le fichier
import xlrd
import MySQLdb

from flask_login import LoginManager, UserMixin
import flask_login
import bcrypt
import hashlib


app = Flask(__name__)
login = LoginManager(app)
app.secret_key = 'many random bytes'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Trucs mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'passer'
app.config['MYSQL_DB'] = 'gestion_logement'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# Trucs de mail
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG']
app.config['MAIL_USERNAME'] = 'groupe4ipdl@gmail.com'
app.config['MAIL_PASSWORD'] = 'passer.1234'
app.config['MAIL_DEFAULT_SENDER'] = 'groupe4ipdl@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHEMENTS'] = False

mail = Mail()
mail.init_app(app)

mysql = MySQL(app)

# Page d'admin des gestionnaires
@app.route('/page_admin/gestionnaire')
def lister_gestionnaires():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, prenom, nom, email, username, fonction, Pavillon_nom_pavillon, numero FROM gestionnaire where etat='activer'")
	rows = cur.fetchall()
	cur.close()
	return render_template('pages_admin/index.html', users = rows)


# Page d'admin des etudiants
@app.route('/page_admin/etudiant')
def gestion_etudiant():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, prenom, nom, niveau, departement, email, nce, cni, date_de_naissance FROM etudiant")
    rows = cur.fetchall()
    cur.close()
    return render_template('pages_admin/gestion_etudiants.html', users = rows)



# Page des gestionnaires
@app.route('/page_gestionnaire')
def index_gestonnaire():
    return render_template("pages_gestionnaire/index.html")


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
        return redirect(url_for('lister_gestionnaires'))


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
    return redirect(url_for('lister_gestionnaires'))


# Modification
@app.route('/<string:user_id>/update', methods = ['POST'])
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
        return redirect(url_for('lister_gestionnaires'))



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
                return redirect(url_for('lister_gestionnaires'))
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



# Envoie mail 
@app.route('/')
def envoiMailEtudiant():
    database = MySQLdb.connect(host="localhost", user="", passwd="", db="")
    cursor = database.cursor()
    cursor.execute("SELECT prenom, nom, email, id FROM etudiant")
    resultat = cursor.fetchall()

    with mail.connect() as conn:
        for e in resultat:
            msg = Message('Reservation 2020', recipients=[e[2]])
            msg.body = 'Salut'+' '+e[0]+' '+e[1]+' Vous pouvez vous inscrire sur le lien suivant pour les besoins de logements du campus social '+'/etudiant/creationcCompte/'+e[3]
            conn.send(msg)

    return 'Message envoyé'


# Recuperation des etudiants
@app.route('/uploadFichier', methods=["POST"])
def uploadFichierInsertion():

    #inputFile = name de l'input de type file
    fichier = request.files['inputFile']

    book = xlrd.open_workbook(fichier.filename)
    sheet = book.sheet_by_name("Feuille1")

    database = MySQLdb.connect(host="localhost", user="test", passwd="passer", db="gestion_logement")

    cursor = database.cursor()

    query = """INSERT INTO etudiant (nom, prenom, niveau, departement, email, telephone, nce, cni, date_de_naissance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    for r in range(1, sheet.nrows):
        nom = sheet.cell(r,0).value
        prenom = sheet.cell(r,1).value
        niveau = sheet.cell(r,2).value
        departement = sheet.cell(r,3).value
        email = sheet.cell(r,4).value
        telephone = sheet.cell(r,5).value
        NCE = sheet.cell(r,6).value
        CNI = sheet.cell(r,7).value
        date_de_naissance = sheet.cell(r,8).value


        values = (nom, prenom, niveau, departement, email, telephone, NCE, CNI, date_de_naissance)

        cursor.execute(query, values)

    cursor.close()
    database.commit()
    database.close()

    return redirect(url_for('gestion_etudiant'))

@app.route('/uploadFichierSuppression', methods=["POST"])

def uploadFichierSuppression():

    #inputFile = name de l'input de type file
    fichier = request.files['inputFile']

    book = xlrd.open_workbook(fichier.filename)
    sheet = book.sheet_by_name("Feuille1")

    database = MySQLdb.connect(host="localhost", user="test", passwd="passer", db="gestion_logement")

    cursor = database.cursor()


    for r in range(1, sheet.nrows):
        nom = sheet.cell(r,0).value
        prenom = sheet.cell(r,1).value
        niveau = sheet.cell(r,2).value
        departement = sheet.cell(r,3).value
        email = sheet.cell(r,4).value
        telephone = sheet.cell(r,5).value
        NCE = sheet.cell(r,6).value
        CNI = sheet.cell(r,7).value
        date_de_naissance = sheet.cell(r,8).value

	cursor.execute("""UPDATE etudiant SET etat = "Desactiver" WHERE nom=%s and prenom=%s and niveau=%s and departement%s and email%s and telephone%s and NCE%s and CNI%s and date_de_naissance%s""", nom, prenom, niveau, departement, email, telephone, NCE, CNI, date_de_naissance)

       
    cursor.close()
    database.commit()
    database.close()

    return redirect(url_for('gestion_etudiant'))

@app.route('/ajoutPavillon', methods=["POST"])
def ajoutPavillon():
    database = MySQLdb.connect(host="localhost", user="", passwd="", db="")
    cursor = database.cursor()

    nombre_chambre = request.form['nombre_chambre']
    nombre_places = request.form['nombre_places']
    nom_pav = request.form['nom_pav']
    cursor.execute("INSERT INTO pavillon (nom_pavillon) VALUES(nom_pav)")
    for r in range(1, nombre_chambre):
        cursor.execute("INSERT INTO chambre (numero_chambre, Pavillon_nom_pavillon) VALUES(%d, %s)",r,nom_pav)

    cursor.close()
    database.commit()
    database.close()

if __name__ == '__main__':
    app.run(debug = True)
