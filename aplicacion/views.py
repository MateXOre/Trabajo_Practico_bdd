from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Datos
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json


#GET DE TODOS
@csrf_exempt 
@require_http_methods(["GET"])
def obtener_datos(request):
    dato = Datos.objects.all()
    lista_Datos = list(dato.values())  
    return JsonResponse(lista_Datos, safe=False)

#GET INDIVIDUAL
@csrf_exempt 
@require_http_methods(["GET"])
def obtener_producto(request, pk):
        dato = Datos.objects.get(pk=pk)
        return JsonResponse({'nombre': dato.nombre, 'descripcion': dato.descripcion, 'valor': str(dato.valor)})

#POST 
@csrf_exempt  
@require_http_methods(["POST"])
def crear_producto(request):
    try:
        data = json.loads(request.body)  
        dato = Datos.objects.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            valor=data['valor']
        )
        return JsonResponse({'id': dato.id, 'nombre': dato.nombre, 'descripcion': dato.descripcion, 'valor': str(dato.valor)}, status=201)
    except KeyError:
        return JsonResponse({'error': 'Faltan datos'}, status=400)

#PUT
@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_producto(request, pk):
    try:
        data = json.loads(request.body)
        dato = Datos.objects.get(pk=pk)
        dato.nombre = data['nombre']
        dato.descripcion = data['descripcion']
        dato.valor = data['valor']
        dato.save()  
        return JsonResponse({'id': dato.id, 'nombre': dato.nombre, 'descripcion': dato.descripcion, 'valor': str(dato.valor)})
    except dato.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except KeyError:
        return JsonResponse({'error': 'Faltan datos'}, status=400)


#DELETE
@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_producto(request, pk):
    try:
        dato = Datos.objects.get(pk=pk)
        dato.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente'})
    except dato.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    
def index(request):
    return render(request, 'templates/app/index.html')