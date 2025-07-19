from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from datetime import datetime

from django.contrib.auth.models import User

from .models import Conversation, Activity, UserProgress, Stage,UserAnswer,ChallengeRecord, UserComment

from .serializers import ConversationSerializer, ActivitySerializer,ChallengeAnswerSerializer, ChallengeRecordSerializer

# PARA GENERACION DE PREGUNTAS
#from .utils.request_openai import  *
from .utils.OpenAI_evaluacion_texto import  *
from .utils.OpenAI_evaluacion_respuesta import  *
from .utils.OpenAI_pregunta_con_opciones import  *

# Para manejo de dificultades
from .utils.stablish_dificulty import  *

#Crear usuario
@api_view(['POST'])
def register_user(request): #MODIFICACION COMPLETA
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Se requiere nombre de usuario y contraseña."}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "El usuario ya existe."}, status=400)

    user = User.objects.create_user(username=username, password=password)


    stages = Stage.objects.all()
    for stage in stages:
        UserProgress.objects.create(
            user = user,
            stage = stage,
            chat_number_reached = 0,
            activity_number_reached = 0
        )
        

    return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)



#Obtener conversaciones y actividades del chat
@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def elements_per_stage(request, etapa_id):
    user = request.user
    print(f"user: {user}")
    conversaciones = Conversation.objects.filter(stage_id=etapa_id).order_by('output_order')
    activities = Activity.objects.filter(stage_id=etapa_id).order_by('output_order')

    #comentarios especificos del usuario en la etapa
    comentarios = UserComment.objects.filter(user_id= user, stage_id=etapa_id).order_by('id')

    conv_serializer = ConversationSerializer(conversaciones, many=True).data

    resultado = []
    actividad_index = 0  
    comentario_index = 0

    for mensaje in conv_serializer:
        #Si tiene es un dialogo que va antes de un comentario, aññade el comentario si es que esta disponible
        if mensaje.get('before_comment') and comentario_index< len(comentarios):
            comentario_usuario = comentarios[comentario_index]
            mensaje['contenido_comentario'] = comentario_usuario.comment
            comentario_index+=1

        #Luego se añade el mensaje tenga o no un comentario
        resultado.append(mensaje)

        #Finalmente si el dialogo ya agregado esta antes de una actividad, se añade ademas a la lista la actividad respondida o no
        if mensaje.get('before_activity') and actividad_index < len(activities):
            actividad = activities[actividad_index]
            actividad_serializada = ActivitySerializer(actividad).data

            # Obtener respuesta del usuario si existe
            respuesta_usuario = UserAnswer.objects.filter(user=user, activity=actividad).first()
            if respuesta_usuario:
                actividad_serializada['respuesta_usuario'] = {
                    "seleccion": respuesta_usuario.answer,
                    "es_correcta": respuesta_usuario.correct
                }
            else:
                actividad_serializada['respuesta_usuario'] = None

            resultado.append(actividad_serializada)
            actividad_index += 1

    return Response(resultado)




#Actualizar informacion de progreso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_progress(request):
    user = request.user
    etapa_id = request.data.get('etapa_id')
    ultimo_chat = request.data['numero_conversacion_alcanzada']
    ultima_actividad_orden_salida = request.data['numero_actividad_alcanzada']
    completada = request.data['final_alcanzado']
    respuesta_usuario = request.data.get('respuesta')

    print(request.data)
    print("== DATOS RECIBIDOS EN EL BACKEND ==")
    print("Usuario:", user)
    print("Etapa ID:", etapa_id)
    print("Último chat mostrado:", ultimo_chat) #ESTO ES EL NUMERO DE ORDEN NO LA ID
    print("Última actividad completada:", ultima_actividad_orden_salida) #ESTO ES EL NUMERO DE ORDEN NO LA ID
    print(f"Respuesta recibida: {respuesta_usuario} y el tipo de dato recibido es {type(respuesta_usuario) }")

    try:
        #Actualizacion de informacion de progreso
        progreso = UserProgress.objects.get(user=user, stage_id=etapa_id)
        progreso.chat_number_reached = ultimo_chat
        progreso.activity_number_reached = ultima_actividad_orden_salida
        progreso.completed = completada
        progreso.save()


        #Guardar respuesta
        if respuesta_usuario:
            print("Hay respuesta de usaurio")
            actividad_obj = Activity.objects.get(output_order=ultima_actividad_orden_salida, stage_id=etapa_id)
            ya_respondida = UserAnswer.objects.filter(user=user, activity=actividad_obj).exists()

            if not ya_respondida:
                print("NO HA SIDO RESPONDIDA")
                UserAnswer.objects.create(
                    user = user,
                    activity = actividad_obj,
                    answer = respuesta_usuario["opcion_selecionada"],
                    correct = respuesta_usuario["acierto"]
                )
        
        return Response({'mensaje': 'Progreso actualizado correctamente'})
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






#Obtener progreso de jugador
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def obtain_progress(request): #MODIFICACION COMPLETA
    user = request.user
    all_progress = UserProgress.objects.filter(user=user)
    data = {}

    for progress in all_progress:
        data[f"etapa_{progress.stage.id}"] = {
            "ultimo_chat_mostrado": progress.chat_number_reached,
            "ultima_actividad_completada": progress.activity_number_reached,
            "final_alcanzado": progress.completed,
            "dificultad" : progress.max_difficulty_reached
        }

    return Response(data)




# ================================== Generacion con OpenIA ==================================

@api_view(['POST'])
def generate_challenge_activity(request): #MODIFICACION COMPLETA
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
            intentos += 1

            if result == True:
                formated = True
                if data.get("idea_imagen") is True:
                    prompt_img = data.get("prompt_busqueda_imagen", "")
                    if prompt_img:
                        url_imagen = obtener_primera_imagen(prompt_img)
                        if url_imagen:
                            data["url_imagen"] = url_imagen
                        else:
                            data["url_imagen"] = None
                    else:
                        data["url_imagen"] = None
                else:
                    data["url_imagen"] = None
   
    print("ENVIANDO: ")
    print(data)
    return Response(data)

@api_view(['POST'])
def review_written_response(request): #MODIFICACION COMPLETA
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
def save_challenge_answer(request): #MODIFICACION COMPLETA
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
    tema_num = int(data.get("topic", 0))
    data["topic"] = tema_map.get(tema_num, "Tema desconocido")

    # Añadir el usuario al registro
    data["user"] = user.id

    # Actualizar dificultad de ser necesario
    check_dificulty(id_etapa=tema_num, usuario=user, dificultad=data["difficulty"], acierto=data["is_correct"])
    print(f"LO QUE SE GUARDARA ES ESTO => {data}")
    serializer = ChallengeAnswerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Respuesta guardada exitosamente"}, status=status.HTTP_201_CREATED)
    else:
        print("Errores en serializer:", serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Obtener datos de mejor desafio
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_best_score(request): #MODIFICACION COMPLETA
    print(request)
    usuario = request.user
    mejor = ChallengeRecord.objects.filter(user=usuario).order_by('-total_score', 'total_duration').first()
    if mejor:
        serializer = ChallengeRecordSerializer(mejor)
        return Response(serializer.data)
    
    
    return Response({
        "total_score": 0,
        "total_duration": None,
        "question_score": 0,
        "max_score": 0,
        "bonus_score": 0,
        "timestamp": None,
    })


# Guardar informacion general de desafio
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_challenge_information(request):    #MODIFICACION COMPLETA
    data = request.data
    
    # Usuario que hizo el desafio
    user = request.user

    try:
        # Puntaje
        total_score = data["total_score"]
        
        question_score = data["question_score"]
        bonus_score = data["bonus_score"]
        max_score = data["max_score"]
        
        # Tiempos
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"])
        total_duration =  end_time-start_time

        #Dificultades
        initial_difficulties = data["initial_difficulties"]
        final_difficulties = data["final_difficulties"]

        registro = ChallengeRecord.objects.create(
                    user = user,
                    total_score = total_score,
                    question_score = question_score,
                    bonus_score = bonus_score,
                    max_score = max_score,
                    start_time = start_time,
                    end_time = end_time,
                    total_duration = total_duration,
                    initial_difficulties = initial_difficulties,
                    final_difficulties = final_difficulties
                )
    
        return Response({"mensaje": "Desafío guardado correctamente"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print("error al guardar informacion")
        print(e)
        return Response({"error": str(e)}, status=400)

# Guardar informacion comentario
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_comment(request):
    data = request.data
    user = request.user

    try:
        registro = UserComment.objects.create(
            user = user,
            stage_id = data["etapa_id"],
            comment = data["comentario"],
        )

        return Response({"mensaje": "comentario guardado correctamente"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("error al guardar informacion")
        print(e)
        return Response({"error": str(e)}, status=400)
    