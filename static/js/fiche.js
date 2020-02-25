

//fonction de controle de la page d'inscription
function validate1() { 

    var msg;

    var str = document.getElementById("Passe1").value;

    var str1 = document.getElementById("Passe2").value;

    var str2 = document.getElementById("prenom").value;

    var str3 = document.getElementById("nom").value;

    var str4 = document.getElementById("mail").value;

    var str5 = document.getElementById("phone").value;

    var str6 = document.getElementById("login").value;

    var str7 = document.getElementById("pav").value;

    var str8 = document.getElementById("fonct").value;


    if (str!="" && str==str1)

        if (str2=="" || str3=="" || str4=="" || str5=="" || str6=="" || str7=="" || str8=="")

            msg = "<p style='color:red'>champ non renseigné.</p>";

        else  
            msg = "<p style='color:green'>Inscription réussie.</p>";

    else if(str=="" || str1=="")

        if (str2=="" || str3=="" || str4=="" || str5=="" || str6=="" || str7=="" || str8=="")

            msg = "<p style='color:red'>champ non renseigné.</p>";

        else            		
            msg = "<p style='color:red'>Veuillez saisir et/ou confirmer le mot de passe .</p>"; 

    else
        if (str2=="" || str3=="" || str4=="" || str5=="" || str6=="" || str7=="" || str8=="")

            msg = "<p style='color:red'>champ non renseigné.</p>";
        else
            msg = "<p style='color:red'>mots de passes non identiques .</p>"; 

    document.getElementById("msg").innerHTML= msg; 

} 

// fonction pour le controle de la page de modification

function validate2() { 

    var msg;

    var str2 = document.getElementById("prenomm").value;

    var str3 = document.getElementById("nomm").value;

    var str4 = document.getElementById("maill").value;

    var str5 = document.getElementById("phonee").value;

    var str6 = document.getElementById("fonct").value;

    var str7 = document.getElementById("pav").value;



    if (str2=="" || str3=="" || str4=="" || str5=="" || str6=="" || str7=="")

        msg = "<p style='color:red'>champ non renseigné.</p>";

    else  
        msg = "<p style='color:green'>modification réussie, s'il n'y a pas d'erreur signalée .</p>";


    document.getElementById("msg").innerHTML= msg; 

 }