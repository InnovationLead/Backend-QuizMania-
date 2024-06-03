from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.question_id} {self.question_text}"

class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    option_number = models.IntegerField()
    option_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.option_text

class QuizAttempt(models.Model):
    attempt_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    score = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.score} point - {self.difficulty} level"

class QuestionAttempt(models.Model):
    attempt = models.ForeignKey(QuizAttempt,on_delete=models.CASCADE)
    question= models.ForeignKey(Question,on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option,on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"answered at {self.answered_at}"

    class Meta:
        # define composite primary key
        constraints = [
            models.UniqueConstraint(fields=['attempt','question'], name='unique_attempt_question')
        ]
        