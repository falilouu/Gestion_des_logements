def Connexion():
    database = MySQLdb.connect(host="localhost", user="", passwd="", db="")
    cursor = database.cursor()
    cursor.execute("""SELECT id, email FROM etudiant""")
    users1 = cursor.fetchall()
    cursor.execute("""SELECT id, email FROM gestionnaire""")
    users2 = cursor.fetchall()

    render_template("login/login.html", user1 = user1, user2 = user2)

#Envoie de mail pour la réinitialisation de mot de passe
def mailReinitialisationMDP():

    table = request.form['table']
    iden = request.form['id']
    msg = Message('Reservation 2020', recipients=['email'])
    msg.body = 'Salut vous pouvez changer votre mot de passe sur le lien suivant '+'/'iden+'/'+table
    mail.send(msg)

    return 'Message envoyé'

#script pour vérifier si le mail existe et enregistrer la table ainsi que l'id
<script>

    function validateForm() 
    {
        var email = document.forms["add_form"]["email"].value;
        
        '{% for user in users1 %}'
            if (email == "{{ user['email'] }}") 
            {
                identification = "{{ user1['id'] }}"
                document.forms["add_form"]["id"].name =identification
                table = 'etudiant'
                document.forms["add_form"]["table"].name =table
                return true;
            }   
        '{% endfor %}'

        '{% for user in users2 %}'
            if (email == "{{ user['email'] }}") 
            {
                identification = "{{ user1['id'] }}"
                document.forms["add_form"]["id"].name =identification
                table = 'gestionnaire'
                document.forms["add_form"]["table"].name =table
                return true;
            }
        '{% endfor %}'

        document.forms["add_form"]["email"].value = "Ce mail n'existe pas";
        document.forms["add_form"]["email"].style.color = "red";
        return false;
} 
    
</script>

# Enregistement du nouveau mdp (il faudra vérifier si le mdp et la confirmation du mdp concordent)
def reinitialisationMDP(identifiant,table):
    cursor = database.cursor()

    mdp = request.form['pwd']
    p=hashlib.sha256(mdp).hexdigest()

    cursor.execute("""UPDATE %s SET pwd WHERE id = %s """,table,identifiant)
        # flash('Data Updtated Successfully')
    cursor.close()
    database.commit()
    database.close()
    #return redirect(url_for('Index'))