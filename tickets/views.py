from django.shortcuts import render
from django.http.response import JsonResponse
from .models import *
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets


# 1 without rest framework and no model query (FBV)
def no_rest_no_model(request):
    guests = [
        {
            "id": 1,
            "name": "ramy",
            "mobile": "1030162226",
            "email": "cnioxxx@gmail.com",
        },
        {
            "id": 2,
            "name": "rania",
            "mobile": "1146975969",
            "email": "rania@gmail.com",
        },
    ]
    # safe = False because it's not a hashable values
    return JsonResponse(guests, safe=False)


# 2 model data default django without rest framework (FBV)
def no_rest_from_model(request):
    # get data from database by query set
    data = Guest.objects.all()
    # create a valid and hashable json response
    response = {"guests": list(data.values("name", "mobile", "email"))}
    # return json response
    return JsonResponse(response)


# 3 function based views
# 3.1 GET POST
# use module api_view and specify the request methods
@api_view(["GET", "POST"])
def FBV_list(request):
    # GIT
    if request.method == "GET":
        # get data from database by query set
        guests = Guest.objects.all()
        # use your serializer that created to suit this data
        # serializer handel data as valid and hashable by passing data to it
        # many = true because data may be more than object
        serializer = GuestSerializer(guests, many=True)
        # return json response from serializer and special status
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    elif request.method == "POST":
        # serializer reverse its jop to deserialization
        # it takes the request data as json and convert it to model type to put it into database(deserialization)
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            # if serializer data is valid for models it would be save
            serializer.save()
            # return response for data modified just for best practice and return status for accepted operation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # return serialize error and status for rejected operation
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3.1 GET PUT DELETE
# use module api_view and specify the request methods
@api_view(["GET", "PUT", "DELETE"])
# function take request data and primary key(id) to specify the object
def FBV_pk(request, pk):
    try:
        # get object data that match the pk givin
        guest = Guest.objects.get(pk=pk)
        # if not exist user model exception does not exist
    except Guest.DoesNotExist:
        # return status not found
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == "GET":
        # get data of object as json format from serializer by passing object data to it
        serializer = GuestSerializer(guest)
        # return serializer data and status ok
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT
    elif request.method == "PUT":
        # serializer get request data and convert it to model formate(deserialization)
        # serializer get guest data to update on it and avoid creating new instance
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            # if data valid save it
            serializer.save()
            # return response of object new data and status accepted
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            # return response of serializer error and status rejected
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == "DELETE":
        # delete object
        guest.delete()
        # return status no content
        return Response(status=status.HTTP_204_NO_CONTENT)


# 4 class based views
# 4.1 GET & POST
# class get module APIView
class CBV_LIST(APIView):
    # function for get take self & request
    def get(self, request):
        # get data from database by query set
        guests = Guest.objects.all()
        # serialize model data and many = true
        serializer = GuestSerializer(guests, many=True)
        # return response of serialized data and status of ok
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # deserialize json request data to model type
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            # if valid save
            serializer.save()
            # return serialize data of modified object in json
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # else return serializer error and status ok
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE
# class get module APIView
class CBV_pk(APIView):
    # get_object function take self & pk
    def get_object(self, pk):
        try:
            # get object data by special pk
            return Guest.objects.get(pk=pk)
        # except by model error does not exist
        except Guest.DoesNotExist:
            # raise error 404
            raise Http404

    # get take self, request, pk
    def get(self, request, pk):
        # get the object data by get_object function that takes the pk
        guest = self.get_object(pk)
        # serialize object data
        serializer = GuestSerializer(guest)
        # return serialized data and status of ok
        return Response(serializer.data, status=status.HTTP_200_OK)

    # put take self, request, pk
    def put(self, request, pk):
        # get object data by get_object function
        guest = self.get_object(pk)
        # deserialize request data
        # take object data to update it by the request deserialized data
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            # if valid save changes
            serializer.save()
            # return response of new object data
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            # else response by serializer error and status rejected
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete function take self, request, pk
    def delete(self, request, pk):
        # get the specified object data by function get_object that takes the pk
        guest = self.get_object(pk)
        # delete object's data
        guest.delete()
        # return response no content
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 mixins list GET POST
# List, Create
class mixins_list(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    # queryset to get data
    queryset = Guest.objects.all()
    # serialize data
    serializer_class = GuestSerializer

    # get function to list data
    def get(self, request):
        return self.list(request)

    # post function to post data
    def post(self, request):
        return self.create(request)


# 5.2 mixins list GET PUT DELETE
# Retrieve, Update, Destroy
class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    # query set to get data
    queryset = Guest.objects.all()
    # serialize data
    serializer_class = GuestSerializer

    # get function to get data, take the pk
    def get(self, request, pk):
        return self.retrieve(request)

    # put function to put data, take the pk
    def put(self, request, pk):
        return self.update(request)

    # delete function to delete data, take the pk
    def delete(self, request, pk):
        return self.destroy(request)


# 6 Generics
# 6.1 GET & POST
class generics_list(generics.ListCreateAPIView):
    # queryset to get data
    queryset = Guest.objects.all()
    # using serializer class
    serializer_class = GuestSerializer


# 6.2 GET & PUT & DELETE
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    # queryset to get data
    queryset = Guest.objects.all()
    # using serializer class
    serializer_class = GuestSerializer


# 7 viewsets
# GET POST PUT DELETE
class viewsets_guest(viewsets.ModelViewSet):
    # queryset to get data
    queryset = Guest.objects.all()
    # using serialize_class
    serializer_class = GuestSerializer
    # apply filter (search)
    filter_backends = [filters.SearchFilter]
    # search field
    search_fields = ["name"]


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
