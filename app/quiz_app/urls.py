from django.urls import path

from .views import question_list,create_question,create_attempt,get_attempts,get_attempt_by_id,create_question_attempt



urlpatterns = [
    path("questions/",view=question_list,name="questions"),
    path("questions/create",view=create_question,name="create_question"),
    path("attempt",view=get_attempts,name="get_attempts"),
    path("attempt/<int:attempt_id>", view=get_attempt_by_id,name="get_attempt_by_id"),
    path("attempt/create",view=create_attempt,name="create_attempt"),
    path("question_attempt/create",view=create_question_attempt,name="create_question_attempt")
]