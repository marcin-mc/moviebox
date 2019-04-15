from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
)

from .models import (
    Comment,
    Movie,
)


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'created',
        ]


class CommentListSerializer(ModelSerializer):
    movie_id = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'movie_id',
            'text',
        ]

    def get_movie_id(self, obj):
        return obj.movies.first().id


class MovieDetailSerializer(ModelSerializer):
    comments = CommentListSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieListSerializer(ModelSerializer):
    comments = SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'comments',
        ]
    
    def get_comments(self, obj):
        return obj.comments.count()


class MovieRankSerializer(ModelSerializer):
    movie_id = SerializerMethodField()
    rank = IntegerField()
    total_comments = SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'movie_id',
            'total_comments',
            'rank',
        ]
    
    def get_total_comments(self, obj):
        return obj.comment_count
    
    def get_movie_id(self, obj):
        return obj.id
