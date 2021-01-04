from django.shortcuts import render
from tablib import Dataset
from person.resources import PersonResource
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from person.models import *
from .serializers import PersonSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class PersonView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        person = Person.objects.all()
        personserializer = PersonSerializer(person, many=True)
        return Response(personserializer.data)

    def post(self, request, *args, **kwargs):
        person_serializer = PersonSerializer(data=request.data)

        if person_serializer.is_valid():
            person_serializer.save()
            return Response(person_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')
