from xml.dom import ValidationErr
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Actor, Movie
from .serializers import ActorSerializer, MovieSerializer

class ActorAPIView(APIView):
    def get(self,request,  *args, **kwargs):
        actor=Actor.objects.all()
        serializer=ActorSerializer(actor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,  *args, **kwargs):
        data=request.data
        if isinstance(data, list):
            serializer= ActorSerializer(data=request.data, many=True)
        elif isinstance(data, dict):
            serializer= ActorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request,*args, **kwargs):
        id=kwargs.get("pk", None)
        if not id:
            return Response(
                ["please provide valid key in the URL"], status=status.HTTP_400_BAD_REQUEST
            )
        else:
            try:
                actor = Actor.objects.get(id=id)
                serializer=ActorSerializer(actor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Actor.DoesNotExist:
                return Response(
                    ["Data Not Found"], status=status.HTTP_404_NOT_FOUND
                )


class MovieAPIView(APIView):
    def get(self, request, *args, **kwargs):
        movie=Movie.objects.all()
        serializer=MovieSerializer(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)