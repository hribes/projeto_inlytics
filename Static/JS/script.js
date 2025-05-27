let olho = document.getElementById("olho");
let senha = document.getElementById("senha");

olho.onclick = function() {
    if (senha.type == "password") {
        senha.type = "text"; 
        olho.src = "/static/Imagens/olho-aberto.png";
    } else {
        senha.type = "password";
        olho.src = "/static/Imagens/olho-fechado.png";
    }
}