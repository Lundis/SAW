from django.db import models

# Create your models here.
class Poll_question(models.Model):
    question_text= models.CharField(max_length=300)
    publication_date = models.DateTimeField('Date published')
    # expiration date

class User_choice(models.Model):
    question = models.ForeignKey(Poll_question)
    choice_text = models.CharField(max_length=300)
    vote_amount = models.IntegerField(default=0)

