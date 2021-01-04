import xlrd
import json
from django.shortcuts import render
from import_export.formats.base_formats import XLS
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from fileapp.models import *
from .serializers import FileSerializer
import openpyxl
from tablib import Dataset
from person.resources import *
from pyexcel_xlsx import get_data


# Create your views here.


class FileView(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        file = File.objects.all()
        fileserializer = FileSerializer(file, many=True)
        return Response(fileserializer.data)

    def post(self, request, format=None, *args, **kwargs):
        datalist = []
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():

            data_list = {'raw': request.data, 'data': request._request.POST,
                          'files': str(request._request.FILES)}
            print(data_list)

            '''pyexcel'''
            file_obj = request.data["file"]
            data = get_data(file_obj)
            for row_initial in data.values():
                for row_final in row_initial[1:]:
                    main_data = row_final
                    print(main_data)
                    p_identity = row_final[0]
                    p_name = row_final[1]
                    p_email = row_final[2]
                    p_birthdate = row_final[3]
                    p_location = row_final[4]
                    print(p_identity, p_name, p_email, p_birthdate, p_location)
            # print(json.dumps(data))
            print("pyexcel")

            '''export-import'''
            # person_resource = PersonResource()
            # print(person_resource)
            # dataset = Dataset()
            # new_persons = request.FILES['file']
            # print(new_persons)
            #
            # imported_data = dataset.load(new_persons.read(), format='xls')
            # print(imported_data)
            # result = person_resource.import_data(dataset, dry_run=True)
            # print(result)
            #
            # if not result.has_errors():
            #     person_resource.import_data(dataset, dry_run=False)  # Actually import now
            #
            # else:
            #     return Response('file parsing error', status=status.HTTP_400_BAD_REQUEST)

            '''openpyxl'''
            excel_file = request.FILES["file"]
            wb = openpyxl.load_workbook(excel_file)

            sheet = wb.active
            rows = sheet.rows
            first_row = [cell.value for cell in next(rows)]
            data = []
            for row in rows:
                record = {}
                for key, cell in zip(first_row, row):
                    if cell.data_type == 's':
                        record[key] = cell.value.strip()
                    else:
                        record[key] = cell.value
                data.append(record)
            print(data)

            for num in data:
                person_identity = num['id']
                person_name = num['name']
                person_email = num['email']
                person_birthdate = num['birth_date']
                person_location = num['location']
                print(person_identity, person_name, person_email, person_birthdate, person_location)

                datalist.append(Person(name=person_name,
                                       email=person_email,
                                       birth_date=person_birthdate,
                                       location=person_location))
                print(datalist)
            if datalist is None:
                return Response(datalist, status=status.HTTP_400_BAD_REQUEST)
            else:
                Person.objects.bulk_create(datalist)

            print("openpyxl")

            worksheet = wb["Sheet1"]
            excel_data = list()

            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    # print(cell, cell.value)
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
            print(excel_data)

            # data = bytes()
            # for chunk in excel_file.chunks():
            #     data += chunk
            # dataset = XLS().create_dataset(data)
            # result = PersonResource().import_data(dataset, dry_run=False, raise_errors=True)
            # print(result)

            '''xlrd'''
            # workbook = xlrd.open_workbook(excel_file, on_demand=True)
            # worksheet = workbook.sheet_by_index(0)
            # first_row = []
            # for col in range(worksheet.ncols):
            #     first_row.append(worksheet.cell_value(0, col))
            # data = []
            # for row in range(1, worksheet.nrows):
            #     record = {}
            #     for col in range(worksheet.ncols):
            #         if isinstance(worksheet.cell_value(row, col), str):
            #             record[first_row[col]] = worksheet.cell_value(row, col).strip()
            #         else:
            #             record[first_row[col]] = worksheet.cell_value(row, col)
            #     data.append(record)
            # print(data)

            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
