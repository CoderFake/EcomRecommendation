from django.db import models


class Embedding(models.Model):
    image_id = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)
    embedding = models.BinaryField()
    faiss_id = models.IntegerField()

    class Meta:
        app_label = "image_embeddings"
