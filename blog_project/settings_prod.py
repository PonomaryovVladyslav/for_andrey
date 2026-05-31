import os

DEBUG = False
ALLOWED_HOSTS = ['3.137.138.185']  # Замените на ваш IP-адрес

# Security for reverse proxy/HTTPS
CSRF_TRUSTED_ORIGINS = ['http://3.137.138.185', 'https://3.137.138.185']  # Замените на ваш IP
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Настройки безопасности для HTTPS (раскомментировать после настройки SSL)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

# Настройки для статики и медиа
STATIC_ROOT = '/home/ubuntu/blog_project/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/home/ubuntu/blog_project/media/'
MEDIA_URL = '/media/'

# Максимальный размер загружаемых файлов (100MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'HOST': os.environ.get('DBHOST', '127.0.0.1'),
        'PORT': os.environ.get('DBPORT', '5432'),
    }
}