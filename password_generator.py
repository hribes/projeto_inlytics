from werkzeug.security import generate_password_hash

senha = "teste123"
senha_hash = generate_password_hash(senha)
print("sua senha é: ",senha_hash)