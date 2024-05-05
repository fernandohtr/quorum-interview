from django.db import models


class Legislator(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Bill(models.Model):
    title = models.CharField(max_length=250)
    sponsor = models.ForeignKey(Legislator, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Vote(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE)


class VoteResult(models.Model):
    class VoteType(models.IntegerChoices):
        SUPPORTES = 1
        OPPOSES = 2

    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=VoteType)
