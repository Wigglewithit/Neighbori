from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class County(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class ZipCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.code