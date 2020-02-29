from flask import Flask , request
from flask_mail import Mail , Message
#pour le fichier
import xlrd
import MySQLdb
app = Flask(__name__)

app.config['DEBUG'] = True
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


@app.route('/')
def envoiMailEtudiant():
	database = MySQLdb.connect(host="localhost", user="", passwd="", db="")
	cursor = database.cursor()
	cursor.execute("SELECT prenom, nom, email FROM etudiant")
	resultat = cursor.fetchall()

	with mail.connect() as conn:
		for e in resultat:
			msg = Message('Reservation 2020', recipients=[e[2]])
			msg.body = 'Salut'+' '+e[0]+' '+e[1]
			conn.send(msg)

	return 'Message envoyé'

def uploadFichierInsertion():
	#inputFile = name de l'input de type file
	fichier = request.files['inputFile']

	book = xlrd.open_workbook(fichier)
	sheet = book.sheet_by_name("source")

	database = MySQLdb.connect(host="localhost", user="", passwd="", db="")

	cursor = database.cursor()

	query = """INSERT INTO orders (nom, prenom, niveau, departement, email, telephone, nce, cni, date_de_naissance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

	for r in range(1, sheet.nrow):
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
 
if __name__ == '__main__':
	app.run()
	