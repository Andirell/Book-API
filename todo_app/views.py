from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoSerializer
from .models import Todos

# Create your views here.
class Todo(APIView):

    def get(self, request):
        todos = Todos.objects.all()

        serializer = TodoSerializer(todos, many=True)
        return Response({"message": "get request successful", "data": serializer.data}, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "post request successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"errors": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            todos = Todos.objects.get(id=id)
        except Todos.DoesNotExist:
            return Response({"message": "put request successful"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todos, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "put request successful"}, status=status.HTTP_200_OK) 
        else:
            return Response({"errors": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, id):
        try:
            todos = Todos.objects.get(id=id)
        except Todos.DoesNotExist:
            return Response({"message": "The todo you are looking for does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        todos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
