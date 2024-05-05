from django.db import models


class Legislator(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Bill(models.Model):
    title = models.CharField(max_length=250)
    sponsor = models.ForeignKey(Legislator, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, blank=True, null=True)


class VoteResult(models.Model):
    class VoteType(models.IntegerChoices):
        SUPPORTES = 1
        OPPOSES = 2

    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, blank=True, null=True)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, blank=True, null=True)
    vote_type = models.IntegerField(choices=VoteType)
