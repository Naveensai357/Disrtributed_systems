from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    voters = models.ManyToManyField(User, related_name='voted_questions', blank=True)

    def __str__(self):
        return self.question_text

    def can_vote(self, user):
        return not self.voters.filter(id=user.id).exists()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text