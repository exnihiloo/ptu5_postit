from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

# def home(request):
#     return render(request, 'postit_api/index.html')

class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentList(generics.ListCreateAPIView):
    # queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Comment.objects.filter(post=post)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can't delete posts not of your own!!!"))


    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can't update posts that are not yours."))


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can't delete comments not of your own!!!"))


    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can't update comments that are not yours."))


class PostLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = models.Post.objects.get(pk = self.kwargs["pk"])
        return models.PostLike.objects.filter(user = user, post = post)


    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already left like on this post!'))
        user = self.request.user
        post = models.Post.objects.get(pk = self.kwargs["pk"])
        serializer.save(user = user, post = post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("You didn't like this post to begin with."))


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        user = User.objects.filter(pk = self.request.user.pk)
        if user.exists():
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('User doesn\'t exist.')