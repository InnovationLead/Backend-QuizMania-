from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import QuestionSerializer, OptionSerializer, QuizAttemptSerializer,QuestionAttemptSerializer
from .models import Question,QuizAttempt
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
        method="get",
    manual_parameters=[
        openapi.Parameter('difficulty', openapi.IN_QUERY, description="Difficulty level", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter('category', openapi.IN_QUERY, description="Category of the questions", type=openapi.TYPE_STRING, required=False)
    ]
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def question_list(request):
    """
    List 20 questions along with their options
    """

    difficulty = request.GET.get('difficulty',None)
    category = request.GET.get('category',None)

    questions = Question.objects.all()
    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    if category:
        questions = questions.filter(category=category)

    serializer = QuestionSerializer(questions.order_by('?')[:20], many=True)
    return Response(serializer.data)


# custom schema for create questions, swagger docs
option_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'option_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='number'),
        'option_text': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN,default=False, description='boolean')
    }
)
options_array_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=option_schema,
    min_items=4,  # Ensure there are at least four options
    max_items=4   # Ensure there are at most four options
)
schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'question_text': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'category': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'difficulty': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'options': options_array_schema
    }
)
@swagger_auto_schema(method='post', request_body=schema)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_question(request):
    """
    Add questions along with the options

    **Permissions:**
        - Requires admin access
    
    **Request Body:**
    """
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        options_data = request.data.pop('options')
        # create and save option in a list
        for option in options_data:
            option_serializer = OptionSerializer(data=option)
            if option_serializer.is_valid():
                option_serializer.save(question=question)
            else:
                return Response(option_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_attempt(request):
    """
    Create a quiz attempt whenever user plays quiz

    **Permissions:**
        - Requires user authentication

    **Request Body:**

    """
    user = request.user
    data = request.data
    data['user'] = user
    serializer = QuizAttemptSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_attempts(request):
    """
    Retrieve all quiz attempts for the currently authenticated user.

    **Permissions:**
        - Requires user authentication.

    **Response:**
        - A JSON response containing a list of serialized quiz attempts
          associated with the authenticated user.
        - Status code: 200 OK
    """
    user = request.user
    attempts = QuizAttempt.objects.all().filter(user=user)
    serializer = QuizAttemptSerializer(attempts,many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_attempt_by_id(request,attempt_id):
    """
    Retrieve a specific quiz attempt by its ID.

    **Permissions:**
        - Requires user authentication.

    **Parameters:**
        - attempt_id (int): The ID of the quiz attempt to retrieve.

    **Response:**
        - On success:
            - A JSON response containing the serialized quiz attempt data.
            - Status code: 200 OK
        - On error:
            - A JSON response with an error message (e.g., "Not found").
            - Status code: 404 Not Found
    """
    user = request.user
    try:
        attempt = QuizAttempt.objects.get(pk=attempt_id)
    except QuizAttempt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if attempt.user != user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = QuizAttemptSerializer(data=attempt)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_question_attempt(request):
    """
    Create a question attempt when user submits the quiz

    **Permissions:**
        - Requires user authentication
    
    """
    