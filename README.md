# Migraciones

python manage.py makemigrations
python manage.py migrate

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

# Cargar seed's (windows shell)
Get-ChildItem -Path ../semillas -Filter *.json | Sort-Object Name | ForEach-Object { python manage.py loaddata $_.FullName }








# Anotaciones

## Cosas que hacer (RECORDAR)
- Terminar de hacer los seeds de 06 contexto falso,07 contenido impostor,08 contenido manipulado,09 contenido fabricado








## Personalidades
1. Irónico, burlón y exagerado. / Ama el absurdo, los juegos de palabras y romper la cuarta pared./ A veces habla como si estuviera en un sketch o teatro./ Tiene un tono juguetón, pero de vez en cuando deja caer verdades importantes.
2. Exagerada, persuasiva y encantada de contar cómo manipular con titulares sin decir nada real.
3. Carismática, convincente y elegante. Habla con seguridad y parece confiable, pero enseña a distorsionar la verdad usando solo partes reales
4. 
5. 
6. 
7. 



## Actividades (ejemplos de estructura)
    {
      "model": "FakeCorp.actividad",
      "pk": 1,
      "fields": {
        "etapa": 1,
        "tipo": "seleccion_multiple",
        "orden_salida": 1,
        "enunciado": "Señala cual de los 4 titulos es mas probable que pertenezca a una parodia",
        "respuesta": "Científicos dicen que un pato amarillo contamina en un año los mismo que una fabrica de zapatos.",
        "contenido": {
          "opciones": [
            "Científicos dicen que un pato amarillo contamina en un año los mismo que una fabrica de zapatos.",
            "Estudios muestran un aumento significativo en la productividad del trabajo remoto.",
            "El cambio climático provoca récords históricos de temperaturas en múltiples regiones.",
            "Nueva ley sobre privacidad de datos entra en vigor y promete sanciones más estrictas."
          ]
        },
        "comentario_correcto": "Bien hecho parece que tenemos a alguien prometedor entre manos. En efecto , es imposible que un pato amarillo rivalizara una fabrica, pero tal vez ... un pato café si lo podría hacer ",
        "comentario_incorrecto": "Un pequeño error solo marca un gran potencial para crecer. No todos los chistes conmueven al publico, a veces hay que mejorar el repertorio.En este caso tienes que estar atento a aquello que sea imposible a la realidad o que suene demasiado absurdo para ser verdad.  En este caso , era imposible que solo un pato hiciera todo eso o no?"
      }
    },

    {
      "model": "FakeCorp.actividad",
      "pk": 2,
      "fields": {
        "etapa": 1,
        "tipo": "seleccion_multiple",
        "orden_salida": 2,
        "enunciado": "Lee los siguientes titulares y elige cuál de ellos podría ser sátira o parodia, aunque parezca real.",
        "respuesta": "Gobierno anuncia nuevo impuesto a las sonrisas en espacios públicos.",
        "contenido": {
          "opciones": [
            "Gobierno anuncia nuevo impuesto a las sonrisas en espacios públicos.",
            "ONU exige medidas urgentes contra la deforestación en la Amazonía.",
            "Ministro de Salud presenta plan nacional de vacunación gratuita.",
            "Economistas alertan sobre inflación en productos alimentarios."
          ]
        },
        "comentario_correcto": "¡Excelente! Has visto la sátira detrás del traje de oficina. ¡Empiezas a tener ojo para el absurdo elegante!",
        "comentario_incorrecto": "¡Ajá! Te atrapó una parodia con pinta de noticia seria. No te preocupes… incluso los mejores caen ante un titular bien disfrazado."
      }
    }




     {
      "model": "FakeCorp.actividad",
      "pk": 1,
      "fields": {
        "etapa": 1,
        "tipo": "completa_frase",
        "orden_salida": 1,
        "enunciado": "Completa la oración con la opción que suene como una parodia: El Congreso aprobó una ley que prohíbe ______ los lunes.",
        "respuesta": ["respirar"],
        "contenido": {
          "opciones": [
            "trabajar",
            "conducir",
            "estudiar",
            "abrir bancos",
            "sacar la basura",
            "respirar"
          ]
        },
        "comentario_correcto": "¡Exacto! Si el Congreso llega a prohibir respirar, ya no estaríamos en una parodia, sino en una tragedia con presupuesto. ¡Bien olfateado, aprendiz!",
        "comentario_incorrecto": "Mmm... esa opción suena casi razonable. Y si algo sabemos de la parodia, es que la lógica se va de vacaciones. ¡Piensa en lo ilógicamente lógico, joven sabio!"
      }
    },

    {
      "model": "FakeCorp.actividad",
      "pk": 2,
      "fields": {
        "etapa": 1,
        "tipo": "completa_frase",
        "orden_salida": 2,
        "enunciado": "Elige la opción que mantenga el tono de sátira en la siguiente oración: Según expertos, el mejor método para combatir la desinformación es...",
        "respuesta": "usar gorros de papel aluminio y bailar alrededor del Wi-Fi.",
        "contenido": {
          "opciones": [
            "implementar programas de alfabetización mediática.",
            "reforzar la regulación en redes sociales.",
            "usar gorros de papel aluminio y bailar alrededor del Wi-Fi.",
            "desarrollar campañas informativas con respaldo científico."
          ]
        },
        "comentario_correcto": "¡Maravillosa locura! Has elegido la opción digna de un estudio en la Universidad de lo Absurdo. Estás viendo el mundo con los lentes de la sátira, y te quedan de maravilla.",
        "comentario_incorrecto": "Oh, oh... caíste en la trampa del sentido común. Pero tranquilo, hasta los mejores detectives del humor se confunden. Intenta buscar la opción que no tendría cabida en un informe serio."
      }
    }