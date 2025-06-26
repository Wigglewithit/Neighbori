from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    # Optional: keep County for later use (just not in UI/forms right now)
    county = models.ForeignKey(
        County,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cities'
    )

    class Meta:
        unique_together = ('name', 'state')  # Still great to keep!

    def __str__(self):
        return f"{self.name}, {self.state.abbreviation or self.state.name}"
