from django.db import models

# Create your models here.
class Produto(models.Model):
    cod = models.CharField(max_length=20, blank=False)
    nome = models.CharField(max_length=50, blank=False)
    unidMedida = models.CharField(max_length=20, blank=False)
    preco = models.CharField(max_length=100, blank=False)
 
    def __str__(self):
        return self.nome

    def get_name(self):
        return self.nome