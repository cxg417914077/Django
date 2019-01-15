from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Students
from django.core.serializers import serialize
import json
from django.http import JsonResponse

# Create your views here.


class StudentsView(View):
    def get(self, request):
        all_students = Students.objects.all()
        data = serialize('json', all_students)
        data = json.loads(data)
        return JsonResponse(data, safe=False, status=200)

    def post(self, request):
        pass
        return HttpResponse('添加成功的对象json', status=201)


class StudentsSingleView(View):
    def get(self, request, pk):
        students_list = Students.objects.filter(id=int(pk))
        data = serialize('json', students_list)
        data = json.loads(data)
        return JsonResponse(data, safe=False, status=200)

    def put(self, request, pk):
        pass
        return HttpResponse('修改成功的对象json', status=201)

    def delete(self, request, pk):
        Students.objects.filter(id=int(pk)).delete()
        return JsonResponse({}, safe=False, status=204)

    def patch(self, request, pk):
        pass
        return HttpResponse('修改成功的对象json', status=201)

