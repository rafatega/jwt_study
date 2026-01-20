import jwt
import datetime

# Minha chave secreta
SECRET_KEY = "segredo-super-seguro" \

# Informações do usuário
payload = {
    "user_id": 123,
    "username": "rafael",
    "role": "admin",
    "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)  # expiração em 1h
}

# Gerando o token (crachá)
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Token JWT:")
print(token)