from django.db import models


class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=260)

    def __str__(self):
        return f"User(name={self.name}, email={self.email}, password={self.password})"


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Task(title={self.title}, description={self.description}, completed={self.completed}, created_at={self.created_at}, due_date={self.due_date})"
