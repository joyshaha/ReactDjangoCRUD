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


class PersonDetail(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    # def get(self, request, *args, **kwargs):
    #     print(args, kwargs)
    #     person = Person.objects.get(pk=kwargs['pk'])
    #     personserializer = PersonSerializer(person)
    #     return Response(personserializer.data)

    def put(self, request, *args, **kwargs):
        print(args, kwargs)
        person = Person.objects.get(pk=kwargs['pk'])
        personserializer = PersonSerializer(person, data=request.data)
        if personserializer.is_valid():
            personserializer.save()
            return Response(data=personserializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=personserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        person = Person.objects.get(pk=kwargs['pk'])
        person_serializer = PersonSerializer(person)
        person.delete()
        return Response(status=status.HTTP_200_OK)


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


'''

def generic_getResponse(model, ModelSerializer, ClassName, pk):
    try:
        modelObject = model.objects.get(pk=pk)
        serializer = ModelSerializer(modelObject)
        return serializer.data
    except model.DoesNotExist:
        message = ClassName + " does not exists"
        response = {
            'success': False,
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'Errors': ''
        }
        return response


def generic_postResponse(ModelSerializer, request, ClassName):
    serializer = ModelSerializer(data=request.data)
    if serializer.is_valid() and len(request.data) > 0:
        # print(serializer.data)
        serializer.save(created_by=request.user)
        mylog.info(request.data)
        message = ClassName + " is created Successfully"
        content = {
            'success': True,
            'statuscode': status.HTTP_200_OK,
            'message': message,
            'Errors': ''
        }
        return content
        # print(serializer.errors)
        message = "Error! Couldn't create new " + ClassName
        response = {
            'success': False,
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'Errors': serializer.errors
        }
        mylog.error(serializer.errors)

        return response


def generic_putResponse(request, model, pk, ModelSerializer, ClassName):
    try:
        modelObject = model.objects.get(pk=pk)
        serializer = ModelSerializer(modelObject, data=request.data, )

        if serializer.is_valid():
            serializer.save(updated_by=request.user, updated_date=datetime.now())
            mylog.info(request.data)
            message = ClassName + " Updated Successfully"
            response = {
                'success': True,
                'statuscode': status.HTTP_200_OK,
                'message': message,
                'Errors': ''
            }
            return response
            message = "Validation error"
            response = {
                'success': False,
                'statuscode': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'Errors': serializer.errors
            }
            mylog.error(serializer.errors)
            return response

    except model.DoesNotExist:
        message = ClassName + ' does not exists'
        response = {
            'success': False,
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'Errors': ''
        }
        return response


def generic_deleteResponse(request, model, pk, ClassName):
    try:
        ModelObject = model.objects.get(pk=pk)
        ModelObject.delete()
        message = ClassName + " Deleted Successfully"
        response = {
            'success': True,
            'statuscode': status.HTTP_200_OK,
            'message': message,
            'Errors': ''
        }
        return response

    except model.DoesNotExist:
        message = ClassName + " does not exists"
        response = {
            'success': False,
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'Errors': ''
        }
        return response


class CountryCodeRUDAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    def get(self, request, pk, format=None):
        return Response(generic_getResponse(model=CountryCode,
                                            ModelSerializer=CountryCodeSerializer,
                                            ClassName="Country Code", pk=pk))


    def put(self, request, pk, format=None):
        return Response(generic_putResponse(request=request,
                                            model=CountryCode, pk=pk,
                                            ModelSerializer=CountryCodeSerializer,
                                            ClassName="Country Code"))


    def delete(self, request, pk, format=None):
        return Response(generic_deleteResponse(request=request,
                                               model=CountryCode, pk=pk,
                                               ClassName="Country Code"))
                                               
'''