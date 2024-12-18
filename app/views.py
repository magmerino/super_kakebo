from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers.user_serializer import UserSerializer
from .serializers.month_serializer import MonthSerializer


@api_view(['POST'])
def post_user(request):
    if request.method == 'POST':
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'error': f'Input data is not formatted correctly. More info: {serializer.errors}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'error': f'Something went wrong creating the user. More info: {ex}'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_by_email(request):
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            user = get_object_or_404(User, email=email)
            serializer = UserSerializer(user)
            return Response({'success': serializer.data}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'error': f'Something went wrong retrieving user. More information: {ex}'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def patch_user(request, identifier):
    try:
        user = get_object_or_404(User, id=identifier)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {'error': f'Something went wrong. Details: {str(ex)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def delete_user(request, identifier):
    try:
        user = get_object_or_404(User, id=identifier)
        user.delete()
        return Response({'success': f'User deleted: {user}'}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response(
            {'error': f'Something went wrong. Details: {str(ex)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

'''
@api_view(['POST'])
def create_month(request):
    if request.method == 'POST':
        serializer = MonthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''