from rest_framework import serializers
from .models import Question,Option,QuestionAttempt,QuizAttempt

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('option_id','option_number','option_text','is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,read_only=True)

    class Meta:
        model = Question
        fields = ('question_id','question_text','category','difficulty','options')
        required = ('question_id','question_text','category','difficulty','options')
    

class QuestionAttemptSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_option = OptionSerializer(read_only=True)

    class Meta:
        model = QuestionAttempt
        fields = ('attempt', 'question', 'selected_option', 'is_correct', 'answered_at')
    
    # def to_representation(self, obj):
    #     return super().to_representation(obj)

class QuizAttemptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    questions_attempted = QuestionAttemptSerializer( many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ('attempt_id', 'user', 'start_time', 'end_time', 'score', 'difficulty', 'questions_attempted')
