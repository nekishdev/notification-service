DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'movies_database'),
        'USER': os.environ.get('DB_USER', 'app'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123qwe'),
        'HOST': os.environ.get('DB_HOST', '62.84.115.122'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'OPTIONS': {
            'options': '-c search_path=public,notify'
        }
    }
}
