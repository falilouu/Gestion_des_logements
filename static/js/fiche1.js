
function validate() { 

    var msg;

    var strr2 = document.getElementById("login1").value;

    var strr3 = document.getElementById("Passe11").value;

    var strr4 = document.getElementById("Passe22").value;
    
    if (strr2=="" || strr3=="" || strr4=="")
        msg = "<p style='color:red'>champ non renseigné.</p>";

    else if (strr3 != strr4)
        msg = "<p style='color:red'>Mots de passe non identiques.</p>";

    else 
        msg = "<p style='color:green'>modification(S) réussie(S).</p>";


    document.getElementById("msg").innerHTML= msg; 

}