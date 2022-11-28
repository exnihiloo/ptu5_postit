from rest_framework import serializers
from . import models



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'body', 'user', 'user_id', 'created_at',)

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    # comments = serializers.StringRelatedField(many=True)
    # many gali grazinti daug rezultatu
    comments = CommentSerializer(many=True, read_only = True)

    class Meta:
        model = models.Post
        fields = (
            'id', 'title', 'image', 'body', 
            'comments_count', 'likes_count', 'comments', 
            'user', 'user_id', 'created_at',
    )

    
    def get_comments_count(self, obj):
        return models.Comment.objects.filter(post=obj).count()

    def get_likes_count(self, obj):
        return models.PostLike.objects.filter(post=obj).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ("id",)
