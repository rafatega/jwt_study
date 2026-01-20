import jwt
import datetime

# Minha chave secreta
SECRET_KEY = "segredo-super-seguro"

# Informações do usuário
payload = {
    "user_id": 123,
    "username": "rafael",
    "role": "admin",
    "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5)  # expiração em 5 segundos
}

# Gerando o token (crachá)
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Token JWT:")
print(token)

# Response: 
# Token JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoicmFmYWVsIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY4OTM1OTEwfQ.1Svc5qQ8u5QumdiTQDHNsaxDlYIdMhaKsGPkg--xF3c