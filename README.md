# JSON Web Token
![JWT Logo](https://jwt.io/img/logo-asset.svg)

---

- [JSON Web Token](#json-web-token)
  - [Introdução](#introdução)
  - [O que é um JWT?](#o-que-é-um-jwt)
  - [Quando usar JWT?](#quando-usar-jwt)
    - [Autorização (o uso mais comum)](#autorização-o-uso-mais-comum)
    - [Troca segura de informações](#troca-segura-de-informações)
  - [Exemplo com Código: Gerar um JWT em Python](#exemplo-com-código-gerar-um-jwt-em-python)
  - [Desmontando o JWT](#desmontando-o-jwt)
    - [O Header](#o-header)
    - [O Payload](#o-payload)
    - [A Secret Key](#a-secret-key)
      - [O que é SECRET\_KEY?](#o-que-é-secret_key)
      - [O que NÃO fazer com SECRET\_KEY:](#o-que-não-fazer-com-secret_key)
      - [Como fazer corretamente?](#como-fazer-corretamente)
      - [Onde guardar a SECRET\_KEY?](#onde-guardar-a-secret_key)
    - [A Signature](#a-signature)
  - [Exemplo visual](#exemplo-visual)
    - [Componentes do JWT](#componentes-do-jwt)
    - [Etapas: passo a passo](#etapas-passo-a-passo)
  - [Por que isso é seguro?](#por-que-isso-é-seguro)


---

## Introdução
JSON Web Token (JWT) é um padrão aberto (RFC 7519) que define uma forma compacta e segura de transmitir informações entre partes como um objeto JSON. Essas informações podem ser verificadas e confiáveis porque são assinadas digitalmente.

---

## O que é um JWT?
Imagine um *crachá digital*. Esse crachá tem:

* O nome da pessoa
* Os acessos que ela tem (ex: pode entrar na sala dos professores, mas não no laboratório)
* E uma assinatura que garante que ninguém falsificou esse crachá

> Esse crachá é o JWT. Ele é entregue para o usuário depois de fazer login, e o usuário mostra esse crachá (o JWT) em toda requisição que fizer.

---

## Quando usar JWT?
### Autorização (o uso mais comum)
Depois que o usuário faz login com e-mail/senha, você dá para ele um JWT. Em cada requisição depois disso, ele manda esse token e, com isso, o sistema sabe *quem ele é* e *o que ele pode acessar*.

*Exemplo do mundo real:*

* Você entra num prédio e recebe um crachá
* Em cada porta que quiser passar, você mostra esse crachá
* O segurança confere o crachá e deixa você entrar se estiver autorizado

> JWT é esse crachá digital.

### Troca segura de informações
Você pode usar JWT para trocar dados entre sistemas diferentes. O JWT pode ser assinado (com uma chave secreta), então quem recebe pode confiar que os dados não foram alterados no caminho.

*Exemplo do mundo real:*

* Um banco envia um contrato assinado digitalmente
* Você sabe que ninguém alterou o contrato porque tem a assinatura digital
* Isso é como um JWT: ele carrega dados e é assinado

---

## Exemplo com Código: Gerar um JWT em Python
<details>
<sumary>Ver código</sumary>

```python
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

# Response: 
# Token JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoicmFmYWVsIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY4OTM1OTEwfQ.1Svc5qQ8u5QumdiTQDHNsaxDlYIdMhaKsGPkg--xF3c
```
</details>

Agora vamos para explicação: Com o JWT importado, tudo parece mágica, mas tem muita lógica por trás, vamos destrinchar juntos!

---

## Desmontando o JWT
```python 
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```
Vamos desmontar isso passo a passo, como se fosse uma máquina de montar tokens:
### O Header
É criado automaticamente, se você não informar, a lib jwt assume isso aqui por padrão:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
Isso define que:
   * O algoritmo de assinatura é `HS256` (HMAC com SHA-256)
   * O tipo do token é `JWT`

Com o header em mãos, ele é codificado em `base64url`:
```python
header_json = json.dumps(header, separators=(',', ':')).encode()
encoded_header = base64url_encode(header_json)
```
Esse `encoded_header` será usado na assinatura final (parte 3)

### O Payload
Esse payload é o *conteúdo principal do token*, com as informações do usuário, permissões, tempo de expiração, etc.

```python
payload = {
    "user_id": 123,
    "username": "joaozin",
    "role": "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}
```

O payload passa pela mesma etapa de codificação `base64url`:
```python
payload_json = json.dumps(payload, separators=(',', ':')).encode()
encoded_payload = base64url_encode(payload_json)
```

Esse `encoded_payload` será usado na assinatura final (parte 3)

### A Secret Key
#### O que é SECRET_KEY?
A SECRET_KEY é uma chave secreta compartilhada usada para:
   * Assinar o token → garantir que ele foi gerado por você
   * Verificar o token → conferir que ninguém alterou o conteúdo
    > Ela precisa ser conhecida apenas pelo servidor.

Se alguém roubar essa chave, pode: 
   * Criar tokens falsos
   * Acessar áreas protegidas do sistema
   * Simular qualquer usuário

#### O que NÃO fazer com SECRET_KEY:
Exemplos de *más práticas:*
```python
SECRET_KEY = "123"
SECRET_KEY = "segredo"
SECRET_KEY = "senha123"
SECRET_KEY = "segredo-super-seguro"
```
> Essas chaves são *curtas, fracas e previsíveis,* ficam vulneráveis a *ataques de força bruta* e *dicionário.*

#### Como fazer corretamente?
Exemplo:
```python
# Use uma chave aleatória, longa e difícil de adivinhar
SECRET_KEY = "S5j@9lkF!3a8Zp$7vT2&QrL9zWm#yN6dXe^HgTnB"
```

Ou melhor ainda: gere dinamicamente com o sistema operacional!

Gerando chave segura em Python:
```python
import secrets

SECRET_KEY = secrets.token_urlsafe(64)
print(SECRET_KEY)
```
> Saída (exemplo): Nbh3UO2a5phY-8EQx9qwldEIBhzIkTpU1FCkUJvOaNBeJ9vDsvJOmv3Cg3xpU43GmD1bZ8SnChZbnLD_N5S_Aw
Essa chave:
   * Tem alta entropia
   * É difícil de quebrar
   * É compatível com Base64Url

#### Onde guardar a SECRET_KEY?
*Nunca* deixe a SECRET_KEY no código-fonte, especialmente em projetos públicos no GitHub!

Soluções seguras:
    * Variáveis de ambiente
    * Serviços de gerenciamento de segredos (ex: AWS Secrets Manager, HashiCorp Vault)

Exemplo com Python + `dotenv`:
`.env`:
```ini
SECRET_KEY=Nbh3UO2a5phY-8EQx9qwldEIBhzIkTpU1FCkUJvOaNBeJ9vDsvJOmv3Cg3xpU43GmD1bZ8SnChZbnLD_N5S_Aw
```
```python
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
```

### A Signature
A assinatura é o que garante a integridade do token. Ela é criada combinando o `encoded_header`, o `encoded_payload` e a `SECRET_KEY` usando o algoritmo especificado (HS256 no nosso caso).

```python
import hmac
import hashlib
signing_input = f"{encoded_header}.{encoded_payload}".encode()
signature = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
encoded_signature = base64url_encode(signature)

jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
print("JWT gerado manualmente:")
print(jwt_token)
```
Ou seja:

  * O header e o payload são convertidos para JSON
  * Depois são codificados em Base64Url
  * Em seguida, concatenados com ponto (.)
  * E aí a assinatura é criada com a chave secreta, usando o algoritmo HS256
> Essa assinatura impede que alguém altere o conteúdo sem invalidar o token!

---

## Exemplo visual
### Componentes do JWT
Digamos que os dados fiquem assim:
```ini
# Header encoded em Base64Url
HEADER  = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# Payload encoded em Base64Url
PAYLOAD = eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9hb3ppbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTc3MzEyMH0

SECRET_KEY = "segredo-super-seguro"
```

Então, a *signature* é feita assim:
```python
signature = HMAC-SHA256(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9hb3ppbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTc3MzEyMH0",
    "segredo-super-seguro"
)
signature_encoded = base64url_encode(signature)
# signature_encoded = SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```
E o JWT final fica assim:
>HEADER.PAYLOAD.SIGNATURE
```ini
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9hb3ppbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcwNTc3MzEyMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Etapas: passo a passo
  1. Criar o `header` → codificar com `Base64Url`
  2. Criar o `payload` → codificar com `Base64Url`
  3. Juntar `header.payload` como string
  4. Gerar o `HMAC-SHA256` dessa string usando a `SECRET_KEY` → isso é a *signature binária*
  5. Codificar a *signature* com `Base64Url`
  6. Juntar tudo → `header.payload.signature`

---

## Por que isso é seguro?
- Porque qualquer alteração no `header` ou `payload` muda a `signature`. Se alguém tentar modificar o token, a assinatura não vai bater quando o servidor verificar, e o token será rejeitado.
Assim, o JWT garante que:
  * O token foi gerado por você (assinatura válida)
  * O conteúdo não foi alterado (integridade garantida)
- Só quem tem a chave secreta consegue gerar a assinatura correta
