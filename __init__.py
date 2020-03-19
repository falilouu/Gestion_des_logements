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



# Page admin pavillon
@app.route('/page_admin/pavillon')
def gestion_pavillon():
    if 'identifiant' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM chambre")
        rows = cur.fetchall()
        cur.close()
        return render_template("pages_admin/gestion_pavillon.html", pavillons = rows)
    else:
        return redirect(url_for("login"))



# Page des gestionnaires
@app.route('/page_gestionnaire')
def index_gestionnaire():
    cur = mysql.connection.cursor()
    cur.execute("SELECT r.id, e.nom, e.prenom, r.date_reservation, r.pavillon_nom_pavillon, r.chambre_numero_chambre FROM reservation r, etudiant e WHERE e.id = r.Etudiant_id ")
    reservations = cur.fetchall()
    cur.close()
    return render_template("pages_gestionnaire/index.html", reservations = reservations)



# Page pour les etudiants
@app.route('/page_etudiant')
def index_etudiant():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM chambre")
    chambres = cur.fetchall()

    cur.execute("SELECT * FROM pavillon")
    pavillons = cur.fetchall()
    cur.close()

    return render_template("pages_etudiant/index.html", pavillons = pavillons, chambres = chambres, user = session['identifiant'])


# Page de creation compte etudiant
@app.route('/etudiant/creationCompte/<int:identifiant>')
def creationCompteEtudiant(identifiant):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM etudiant WHERE id =%s ",(identifiant,))
    user = cur.fetchone()

    return render_template("pages_etudiant/registerEtudiant.html", user = user)




# Page de creation compte etudiant
@app.route('/registerEtudiant/<int:identifiant>', methods=['GET', 'POST'])
def registerEtudiant(identifiant):
    tab=[]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM etudiant WHERE id =%s ",(identifiant,))
    user=cur.fetchone()
    cur.execute("SELECT login, email FROM etudiant ")
    tab.append(cur.fetchone()['login'])
    tab.append(cur.fetchone()['email'])
    cur.execute("SELECT username,email FROM gestionnaire")
    tab.append(cur.fetchone()['email'])
    # tab.append(cur.fetchone()['username'])
    cur.execute("SELECT username,login FROM administrateur")
    #tab.append(cur.fetchone()['login'])
    tab.append(cur.fetchone()['username'])
    cur.close()
    
        
    if request.method == "GET":
        
        
        if user!=None:
            
            return render_template("pages_etudiant/registerEtudiant.html",user=user,tab=tab)
    else:
        
        curs = mysql.connection.cursor()
        details = request.form
        login = details['username']
        mdp = details['mdp'].encode("utf-8")
        identifiant = user['id']
        pw_hash =hashlib.sha256(mdp).hexdigest()
        cure = mysql.connection.cursor()
        cure.execute("SELECT * FROM etudiant e,gestionnaire g,administrateur a WHERE a.login=%s  or a.username=%s  or e.email=%s  or e.login=%s or g.email=%s  or g.username=%s   ",(login,login,login,login,login,login,))
        usere=cure.fetchone()
        cure.close()

        if usere==None:
            pw_hash =hashlib.sha256(mdp).hexdigest()
            curs.execute("UPDATE etudiant SET  mdp=%s,login=%s WHERE id = %s",(pw_hash,login,identifiant,))
            #users=curs.fetchone()
            #curs.close()
            mysql.connection.commit()
            flash( "Data Updtated Successfully")
        else:
            return 'Cet identifiant existe deja'
        
        #hash_password=bcrypt.hashpw(mdp,bcrypt.gensalt())

        
        
    cur.close()
    return redirect(url_for('login'))
    #return render_template('login.html')





# Ajout de gestionnaire ou comptable 
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
        identifiant=email
        pw_hash =hashlib.sha256(mdp).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM etudiant e,gestionnaire g,administrateur a WHERE  a.login=%s  or a.username=%s  or e.email=%s  or e.login=%s or g.email=%s  or g.username=%s ",(identifiant,identifiant,identifiant,identifiant,identifiant,identifiant,))
        user=cur.fetchone()
        cur.close()

        if user==None:

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO gestionnaire(nom,prenom,mdp,fonction,etat,email,username,pavillon_nom_pavillon, numero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nom, prenom, mdp, fonction, "Activer", email, username, pavillon, numero))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('lister_gestionnaires'))


# Suppression gestionnaire
@app.route('/user/<string:user_id>/delete', methods = ['POST'])
def delete(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
    UPDATE gestionnaire
    SET etat = "Desactiver"
    WHERE id = %s
    """, (user_id,))
    mysql.connection.commit()
    #cur.close()
    return redirect(url_for('lister_gestionnaires'))


# Modification gestionnaire
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



# Login des users
@login_manager.user_loader
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login/login.html")
    if request.method == "POST":
        
        details = request.form
        identifiant =  request.form['identifiant']
        mdp = details['mdp'].encode("utf-8")
        
        
        cur=mysql.connection.cursor()

        #Connexion étudiant
        cur.execute("SELECT * FROM etudiant WHERE (login =%s or email=%s) and etat=%s",(identifiant,identifiant,"Activer",))
        user=cur.fetchone()
       
        p=hashlib.sha256(mdp).hexdigest()
       
        if user!=None:
            if p == user['mdp']:
                session['identifiant'] = user['id']
                session['prenom'] = user['prenom']
                return redirect(url_for("index_etudiant"))

        # Connexion gestionnaire
        cur.execute("SELECT * FROM gestionnaire WHERE (email =%s or username=%s) and etat=%s",(identifiant,identifiant,"Activer",))
        user=cur.fetchone()
        
        # p=hashlib.sha256(mdp).hexdigest() 
       
        if user!=None:
            mdp = mdp.decode("utf-8")
            if mdp == user['mdp']:
                session['identifiant'] = user['username']
                session['prenom'] = user['prenom']

                if user['fonction'] == "Chef de pavillon":
                    return render_template("pages_gestionnaire/index.html", user = user)
                else:
                    return render_template("pages_comptable/index.html", user = user)

        # Connexion administrateur
        cur.execute("SELECT * FROM administrateur WHERE login =%s or username=%s",(identifiant,identifiant,))
        user=cur.fetchone()
        cur.close()
        p=hashlib.sha256(mdp).hexdigest()
       
        
        if user != None:
            if p==user['mdp']:
                session['identifiant'] = user['username']
                session['prenom'] = user['prenom']
                return render_template("pages_admin/index.html")
        else:
            return "mot de passe incorrecte"

           
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


# Deconnexion
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
            msg.body = 'Salut'+' '+e[0]+' '+e[1]+' Vous pouvez vous inscrire sur le lien suivant pour les besoins de logements du campus social '+'/etudiant/creationCompte/'+e[3]
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

# Supprimer etudiants
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
        
        cursor.execute("""UPDATE etudiant SET etat = "Desactiver" WHERE nom = %s and prenom = %s and niveau = %s and departement = %s and email = %s and telephone = %s and NCE = %s and CNI = %s and date_de_naissance = %s """, (nom, prenom, niveau, departement, email, telephone, NCE, CNI, date_de_naissance))

       
    cursor.close()
    database.commit()
    database.close()

    return redirect(url_for('gestion_etudiant'))


# Ajout de pavillon
@app.route('/ajoutPavillon', methods=["POST"])
def ajoutPavillon():
    database = MySQLdb.connect(host="localhost", user="test", passwd="passer", db="gestion_logement")
    cursor = database.cursor()

    nombre_chambre = request.form['nombre_chambre']
    nombre_places = request.form['nombre_places']
    nom_pav = request.form['nom_pav']
    nombre_chambre = int(nombre_chambre)
    cursor.execute("INSERT INTO pavillon (nom_pavillon) VALUES(%s)", (nom_pav,))
    for r in range(1, nombre_chambre):
        cursor.execute("INSERT INTO chambre (numero_chambre, Pavillon_nom_pavillon, nombre_places, nombre_places_dispo) VALUES(%s, %s, %s, %s)",( r, nom_pav, nombre_places, nombre_places))

    cursor.close()
    database.commit()
    database.close()

    return redirect(url_for('gestion_pavillon'))


# Enregistrer reservation
@app.route('/ajoutReservation', methods=["POST"])
def ajoutReservation():
    pavillon = request.form['pavillon']
    numero_chambre = request.form['numero_chambre']
    etudiant_id = session['identifiant']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reservation WHERE Etudiant_id = %s AND Pavillon_nom_pavillon = %s AND Chambre_numero_chambre = %s", (etudiant_id, pavillon, numero_chambre))

    query = cur.fetchone()
    cur.close()

    if query == None:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reservation (date_reservation, Etudiant_id, Pavillon_nom_pavillon, Chambre_numero_chambre ) VALUES (NOW(), %s, %s, %s)", (etudiant_id, pavillon, numero_chambre))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index_etudiant'))
    else:
        return redirect(url_for('index_etudiant'))


if __name__ == '__main__':
    app.run(debug = True)