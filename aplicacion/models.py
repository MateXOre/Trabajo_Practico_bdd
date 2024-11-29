from django.db import models
from bson import ObjectId

# Modelo SQL
class Datos(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

# Modelo NoSQL
class DatosNoSQL:
    def __init__(self, collection):
        self.collection = collection

    @classmethod
    def create(cls, nombre, descripcion, valor, metadata):
        documento = {
            'nombre': nombre,
            'descripcion': descripcion,
            'valor': float(valor),
            'metadata': metadata or {}
        }
        return documento

    def save(self, documento):
        if '_id' not in documento:
            resultado = self.collection.insert_one(documento)
            documento['_id'] = str(resultado.inserted_id)
        else:
            documento_id = ObjectId(documento['_id'])
            self.collection.replace_one({'_id': documento_id}, documento)
        return documento

    def get_by_id(self, documento_id):
        return self.collection.find_one({'_id': ObjectId(documento_id)})

    def get_all(self):
        return list(self.collection.find())

    def delete(self, documento_id):
        self.collection.delete_one({'_id': ObjectId(documento_id)})