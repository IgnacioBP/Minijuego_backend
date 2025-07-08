from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from datetime import datetime

from django.contrib.auth.models import User
from .models import Conversation, Actividad, UserProgress, Etapa,UserAnswer,RegistroDesafio
from .serializers import ConversationSerializer, ActividadSerializer,RespuestaDesafioSerializer, RegistroDesafioSerializer

# PARA GENERACION DE PREGUNTAS
#from .utils.request_openai import  *
from .utils.OpenAI_evaluacion_texto import  *
from .utils.OpenAI_evaluacion_respuesta import  *
from .utils.OpenAI_pregunta_con_opciones import  *

# Para manejo de dificultades
from .utils.stablish_dificulty import  *

#Crear usuario
@api_view(['POST'])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Se requiere nombre de usuario y contraseña."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "El usuario ya existe."}, status=400)

    user = User.objects.create_user(username=username, password=password)


    etapas = Etapa.objects.all()
    for etapa in etapas:
        UserProgress.objects.create(
            usuario=user,
            etapa=etapa,
            numero_conversacion_alcanzada=0,
            numero_actividad_alcanzada=0
        )
        

    return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)



#Obtener conversaciones y actividades del chat
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def elementos_por_etapa(request, etapa_id):
    user = request.user
    print(f"user: {user}")
    conversaciones = Conversation.objects.filter(etapa_id=etapa_id).order_by('orden_salida')
    activities = Actividad.objects.filter(etapa_id=etapa_id).order_by('orden_salida')

    conv_serializer = ConversationSerializer(conversaciones, many=True).data

    resultado = []
    actividad_index = 0  

    for mensaje in conv_serializer:
        resultado.append(mensaje)

        if mensaje.get('antes_actividad') and actividad_index < len(activities):
            actividad = activities[actividad_index]
            actividad_serializada = ActividadSerializer(actividad).data

            # Obtener respuesta del usuario si existe
            respuesta_usuario = UserAnswer.objects.filter(usuario=user, actividad=actividad).first()
            if respuesta_usuario:
                actividad_serializada['respuesta_usuario'] = {
                    "seleccion": respuesta_usuario.respuesta,
                    "es_correcta": respuesta_usuario.buena
                }
            else:
                actividad_serializada['respuesta_usuario'] = None

            resultado.append(actividad_serializada)
            actividad_index += 1

    return Response(resultado)





#Obtener una sola  actividad para renderizar
@api_view(['GET'])
def single_activity(request, etapa_id, activity_id):
    try:
        activity = Actividad.objects.get(id=activity_id, etapa_id=etapa_id)
        serializer = ActividadSerializer(activity)
        return Response(serializer.data)
    except Actividad.DoesNotExist:
        return Response({"error": "Actividad no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    








#Actualizar informacion de progreso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_progreso(request):
    user = request.user
    etapa_id = request.data.get('etapa_id')
    ultimo_chat = request.data['numero_conversacion_alcanzada']
    ultima_actividad_orden_salida = request.data['numero_actividad_alcanzada']
    compeltada = request.data['final_alcanzado']
    respuesta_usuario = request.data.get('respuesta')

    print(request.data)
    print("== DATOS RECIBIDOS EN EL BACKEND ==")
    print("Usuario:", user)
    print("Etapa ID:", etapa_id)
    print("Último chat mostrado:", ultimo_chat) #ESTO ES EL NUMERO DE ORDEN NO LA ID
    print("Última actividad completada:", ultima_actividad_orden_salida) #ESTO ES EL NUMERO DE ORDEN NO LA ID
    print(f"Respuesta recibida: {respuesta_usuario} y el tipo de dato recibido es {type(respuesta_usuario) }")

    try:
        #ACtualizacion de informacion de progreso
        progreso = UserProgress.objects.get(usuario=user, etapa_id=etapa_id)
        progreso.numero_conversacion_alcanzada = ultimo_chat
        progreso.numero_actividad_alcanzada = ultima_actividad_orden_salida
        progreso.completado = compeltada
        progreso.save()


        #Guardar respuesta
        if respuesta_usuario:
            print("Hay respuesta de usaurio")
            actividad_obj = Actividad.objects.get(orden_salida=ultima_actividad_orden_salida, etapa_id=etapa_id)
            ya_respondida = UserAnswer.objects.filter(usuario=user, actividad_id=actividad_obj).exists()

            if not ya_respondida:
                print("NO HA SIDO RESPONDIDA")
                UserAnswer.objects.create(
                    usuario = user,
                    actividad = actividad_obj,
                    respuesta = respuesta_usuario["opcion_selecionada"],
                    buena = respuesta_usuario["acierto"]
                )
        
        return Response({'mensaje': 'Progreso actualizado correctamente'})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#Obtener progreso de jugador
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_progreso(request):
    user = request.user
    progresos = UserProgress.objects.filter(usuario=user)
    data = {}

    for progreso in progresos:
        data[f"etapa_{progreso.etapa.id}"] = {
            "ultimo_chat_mostrado": progreso.numero_conversacion_alcanzada,
            "ultima_actividad_completada": progreso.numero_actividad_alcanzada,
            "final_alcanzado": progreso.completado,
            "dificultad" : progreso.dificultad_maxima_alcanzada
        }

    return Response(data)








# ================================== Generacion con OpenIA ==================================

@api_view(['POST'])
def generar_actividad_desafio(request):
    print("Solicitud recibida para generar pregunta en desafío")

    question_category = request.data.get('category')
    question_level = request.data.get('lvl')
    question_type = request.data.get('question_type')

    print("Categoría:", question_category)
    print("Nivel:", question_level)
    print("Tipo:", question_type)

    formated = False
    max_intentos = 3
    intentos = 0
    data = None

    if question_type == "escribir_respuesta":
         print("NUVOO FORMATO")
         while not formated and intentos < max_intentos:
            contenido = generate_news_for_title(question_category,question_level)
            print(contenido)
            intentos += 1
            if isinstance(contenido, str):
                data = {"contenido" : contenido} 
                formated = True
    else:
         while not formated and intentos < max_intentos:
            data = obtener_actividad(question_category, question_level,question_type)
            result = check_json(data)
            if result == True:
                formated = True
   
    print("ENVIANDO: ")
    print(data)
    return Response(data)

@api_view(['POST'])
def revisar_respuesta_redactada(request):
    noticia = request.data.get('noticia')
    user_answer = request.data.get('respuesta')
    tema_noticia = request.data.get('tema')

    formated = False
    max_intentos = 3
    intentos = 0
    data = None

    while not formated and intentos < max_intentos:  
        data = evaluate_title_response(noticia, user_answer, tema_noticia)
        print("DEVUELTA DE LA FUNCIOn")
        intentos += 1
        result, situation = check_title_evaluation(data)
        if result:
            print("PASO EVALUACION")
            formated = True 
        else:
            print(situation)
    
    return Response(data)



#===================================================================================================

# GUARDAR PREGUNTAS Y RESPEUSTA DE JUGADOR
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def guardar_respuesta_desafio(request):
    print("Recibida solicitud para guardar informacion de desafio")
    print(request.data)  # Esto imprime lo que realmente llega

    tema_map = {
        1: "Parodia",
        2: "Contenido engañoso",
        3: "Contenido impostor",
        4: "Conexión falsa",
        5: "Contenido manipulado",
        6: "Contexto falso",
        7: "Contenido fabricado"
    }

    user = request.user
    data = request.data.copy()

    # Convertir tema numérico a texto
    tema_num = int(data.get("tema", 0))
    data["tema"] = tema_map.get(tema_num, "Tema desconocido")

    # Añadir el usuario al registro
    data["usuario"] = user.id

    # Actualizar dificultad de ser necesario
    check_dificulty(id_etapa=tema_num, usuario=user, dificultad=data["dificultad"], acierto=data["es_correcta"])

    serializer = RespuestaDesafioSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Respuesta guardada exitosamente"}, status=status.HTTP_201_CREATED)
    else:
        print("Errores en serializer:", serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Obtener datos de mejor desafio
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_mejor_puntaje(request):
    print(request)
    usuario = request.user
    mejor = RegistroDesafio.objects.filter(usuario=usuario).order_by('-puntaje_obtenido', 'tiempo_total').first()
    if mejor:
        serializer = RegistroDesafioSerializer(mejor)
        return Response(serializer.data)
    
    print("default")
    return Response({
        "puntaje_obtenido": 0,
        "tiempo_total": None,
        "puntaje_preguntas": 0,
        "puntaje_tiempo": 0,
        "puntaje_maximo": 0,
        "timestamp": None,
    })


# Guardar informacion general de desafio
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def guardar_informacion_desafio(request):
    data = request.data
    
    # Usuario que hizo el desafio
    user = request.user

    try:
        # Puntaje
        puntaje_obtenido = data["puntaje_obtenido"]
        
        puntaje_preguntas = data["puntaje_preguntas"]
        puntaje_bono_tiempo = data["puntaje_tiempo"]
        puntaje_maximo_preguntas = data["puntaje_maximo"]
        
        # Tiempos
        tiempo_inicio = datetime.fromisoformat(data["hora_inicio"])
        tiempo_termino = datetime.fromisoformat(data["hora_termino"])
        duracion_total =  tiempo_termino-tiempo_inicio

        #Dificultades
        dif_iniciales = data["dificultades_iniciales"]
        dif_finales = data["dificultades_finales"]

        registro = RegistroDesafio.objects.create(
                    usuario=user,
                    puntaje_obtenido=puntaje_obtenido,
                    puntaje_preguntas=puntaje_preguntas,
                    puntaje_tiempo=puntaje_bono_tiempo,
                    puntaje_maximo=puntaje_maximo_preguntas,
                    hora_inicio=tiempo_inicio,
                    hora_termino=tiempo_termino,
                    tiempo_total=duracion_total,
                    dificultades_iniciales=dif_iniciales,
                    dificultades_finales=dif_finales
                )
    
        return Response({"mensaje": "Desafío guardado correctamente"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print("error al guardar informacion")
        print(e)
        return Response({"error": str(e)}, status=400)
