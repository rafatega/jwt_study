import jwt
import datetime
import time

SECRET_KEY = "segredo-super-seguro"

tokens = []

# gera 3 tokens rapidamente
for i in range(6):
    payload = {
        "user_id": 123,
        "username": "rafael",
        "role": "admin",
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    tokens.append(token)
    time.sleep(1)  # só pra diferenciar os exp e deixar visível

print("\nTokens gerados:")
for t in tokens:
    print(t)

print("\nValidando imediatamente:")
for idx, t in enumerate(tokens, 1):
    try:
        decoded = jwt.decode(t, SECRET_KEY, algorithms=["HS256"])
        print(f"Token {idx}: ✅ válido | exp = {decoded['exp']}")
    except jwt.ExpiredSignatureError:
        print(f"Token {idx}: ❌ expirado")
    except jwt.InvalidTokenError:
        print(f"Token {idx}: ❌ inválido")
