from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Tutor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='tutor_images/', blank=True, null=True)
    subjects = models.ManyToManyField('Subject', related_name='tutors')

    def __str__(self):
        return self.name

class Subject(models.Model):
    CATEGORIES = [
        ("math", "Math"),
        ("reading", "Reading/Writing/Language"),
        ("science", "Science")
    ]
    name = models.CharField(max_length=100)
    id = models.CharField(primary_key=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="math")

    def __str__(self):
        return self.name

class Review(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.tutor.name} - Rating: {self.rating}"