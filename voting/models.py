from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    password = models.CharField(max_length=50, default="12345") # Nayi line add ho gayi hai
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Voter(models.Model):
    name = models.CharField(max_length=100)
    enrollment_no = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vote(models.Model):
    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    def __str__(self):
        return f"{self.voter.name} -> {self.candidate.name}"


class ElectionStatus(models.Model):
    is_active = models.BooleanField(default=False)


class ElectionApplication(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return self.name