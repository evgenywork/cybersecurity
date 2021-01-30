ALLOWED_HOSTS = ['*']
DEBUG = True
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'pvt',
    #     'USER': 'progDBqms',
    #     'PASSWORD': 'Prog738tA',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    # },
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'document_recognition',
       'USER': 'postgres',
       'PASSWORD': 'Admin2020#',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   },
}
