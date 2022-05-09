from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Actor, Movie
from .serializers import ActorSerializer

class ActorAPIView(APIView):
    # def get(self,request,  *args, **kwargs):
    #     actor=Actor.objects.all()
    #     serializer=ActorSerializer(actor, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,  *args, **kwargs):
        print("post request", request.data)
        data=request.data
        if isinstance(data, list):
            serializer= ActorSerializer(data=request.data, many=True)
        elif isinstance(data, dict):
            serializer= ActorSerializer(data=request.data)
        print("serializer.is_valid():", serializer.is_valid())
        # print('serializer:', serializer)
        if serializer.is_valid():
            print("serializer.data:", serializer.validated_data)
            serializer.save()
        else:
            # print(serializer._errors)
            return Response(serializer._errors)
        return Response(serializer.data, status=status.HTTP_200_OK)



# {
#        "actor_name": ""
# }