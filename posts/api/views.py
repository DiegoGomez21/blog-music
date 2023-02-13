from django.db.models import Q #Funciona con consulta de filtro avanzado,  permite crear consultas complejas
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post
from posts.api.serializers import PostSerializer
from posts.api.permissions import IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination

class PostApiViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        userr = self.request.user
        if userr.is_superuser:
            return self.queryset
        else:
            #Va a retornar los post que estan publicados y que le pertenecen al usuario
            return self.queryset.filter(Q(published=True) | Q(user=userr.id))
        

    