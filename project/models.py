from django.db import models

PROJECT_CATEGORIES = {
    "WEB_DEV": "Web Development",
    "SYS_DESIGN": "System Design",
    "TALK": "Talk",
}


class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=PROJECT_CATEGORIES)
    short_summary = models.TextField()

    role = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    stack = models.CharField(max_length=100)
    repository = models.URLField(blank=True)

    challenge = models.TextField()
    key_features = models.TextField()
    description = models.TextField()

    image = models.ImageField(upload_to="projects/")

    def __str__(self) -> str:
        return str(self.title)
