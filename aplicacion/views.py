from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Datos, DatosNoSQL
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json
from django.conf import settings

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

# Vistas NoSQL con PyMongo
@csrf_exempt 
@require_http_methods(["GET"])
def obtener_datos_nosql(request):
    if settings.MONGO_DATABASE['datos'] is None:
        return JsonResponse({'error': 'Error de conexión a la base de datos'}, status=500)
    
    datos = DatosNoSQL(settings.MONGO_DATABASE['datos']).get_all()
    
    # Convertir ObjectId a string para serialización JSON
    for dato in datos:
        dato['_id'] = str(dato['_id'])
    
    return JsonResponse(datos, safe=False)

@csrf_exempt 
@require_http_methods(["GET"])
def obtener_producto_nosql(request, pk):
    try:
        dato = DatosNoSQL(settings.MONGO_DATABASE['datos']).get_by_id(pk)
        
        if dato:
            dato['_id'] = str(dato['_id'])
            return JsonResponse(dato)
        else:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt  
@require_http_methods(["POST"])
def crear_producto_nosql(request):
    try:
        data = json.loads(request.body)
        datos_nosql = DatosNoSQL(settings.MONGO_DATABASE['datos'])
        metadata = data.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}
        
        documento = datos_nosql.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            valor=data['valor'],
            metadata=metadata
        )
        
        documento_guardado = datos_nosql.save(documento)
        
        return JsonResponse({
            '_id': documento_guardado['_id'], 
            'nombre': documento_guardado['nombre'], 
            'descripcion': documento_guardado['descripcion'], 
            'valor': str(documento_guardado['valor']),
            'metadata': documento_guardado.get('metadata', {})
        }, status=201)
    except KeyError as e:
        return JsonResponse({'error': f'Falta el campo: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["PUT"])
def actualizar_producto_nosql(request, pk):
    try:
        data = json.loads(request.body)
        datos_nosql = DatosNoSQL(settings.MONGO_DATABASE['datos'])        
        
        documento = datos_nosql.get_by_id(pk)
        
        if not documento:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        
        metadata = data.get('metadata', {})

        if not isinstance(metadata, dict):
            metadata = {}
        
        documento['nombre'] = data['nombre']
        documento['descripcion'] = data['descripcion']
        documento['valor'] = data['valor']
        documento['metadata'] = metadata
        
        documento_actualizado = datos_nosql.save(documento)
        
        return JsonResponse({
            '_id': str(documento_actualizado['_id']), 
            'nombre': documento_actualizado['nombre'], 
            'descripcion': documento_actualizado['descripcion'], 
            'valor': str(documento_actualizado['valor']),
            'metadata': documento_actualizado.get('metadata', {})
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_producto_nosql(request, pk):
    try:
        DatosNoSQL(settings.MONGO_DATABASE['datos']).delete(pk)
        return JsonResponse({'message': 'Producto eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)