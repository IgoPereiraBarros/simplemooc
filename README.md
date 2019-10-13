# Plataforma de Cursos - Simplemooc

## Como rodar o projeto ?

* Clone o repositório.
* Crie uma virtualenv com python 3.
* Ative a virtualenv.
* Instale as dependências.
* configure seu banco de dados
* Rode as migrações.

```
git clone https://github.com/IgoPereiraBarros/simplemooc.git
cd simplemooc
python3 -m venv .venv
pip install -r requirements.txt
python contrib/env_gen.py

No settings.py modifique o dicionário DATABASES, caso queira usar Mysql:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PW',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```