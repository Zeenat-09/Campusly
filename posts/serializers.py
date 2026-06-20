from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username', read_only=True
    )
    likes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    reshared_from_username = serializers.SerializerMethodField()
    reshared_from_content = serializers.SerializerMethodField()
    original_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'content', 'image',
                  'created_at', 'likes_count', 'comments',
                  'reshared_from', 'reshared_from_username',
                  'reshared_from_content', 'original_comments']
        read_only_fields = ['author', 'created_at']

    def get_original_post(self, obj):
        # Keep going back until we find the original post
        while obj.reshared_from:
            obj = obj.reshared_from
        return obj

    def get_likes_count(self, obj):
        original = self.get_original_post(obj)
        return original.likes.count()

    def get_comments(self, obj):
        original = self.get_original_post(obj)
        comments = original.comments.all()
        return CommentSerializer(comments, many=True).data

    def get_reshared_from_username(self, obj):
        if obj.reshared_from:
            return obj.reshared_from.author.username
        return None

    def get_reshared_from_content(self, obj):
        if obj.reshared_from:
            original = self.get_original_post(obj)
            return original.content
        return None

    def get_original_comments(self, obj):
        if obj.reshared_from:
            original = self.get_original_post(obj)
            comments = original.comments.all()
            return CommentSerializer(comments, many=True).data
        return []