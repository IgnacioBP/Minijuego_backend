
# Vaciar las tabla
python manage.py flush

Esto:
-Borra todos los datos de todas las tablas.
-No elimina las tablas ni las migraciones.
-Te deja con una base vacía, como recién creada.



# Crear un solo usaurio (para las pruebas)
python manage.py shell

from django.contrib.auth.models import User

User.objects.create_user(username='usuario_prueba', password='1234')

# Cargar seed
python manage.py loaddata seed.json