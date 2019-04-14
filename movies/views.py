"""
Views and endpoints handled:
    CommentAPIView:
        POST /comments
        GET /comments [?<movie=id>]
    MovieAPIView:
        POST /movies
        GET /movies [?<genre=genrename>][?<director=directorname>]
    MovieDeleteUpdateAPIView:
        DELETE /movies/<movie-id>
        UPDATE /movies/<movie-id>
    MovieTopAPIView:
        GET /top?from=<yyyy-mm-dd>&to=<yyyy-mm-dd>

"""
import json
from datetime import datetime

from django.db.models import Count, F, Q, Window
from django.db.models.functions import DenseRank
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from .models import (
    Comment,
    Movie,
)
from .serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    MovieRankSerializer,
)
from .utils import fetch_movie


class NoDateRangeException(Exception):
    """ Raised by MovieTopAPIView when `from` or `to` is missing """
    
    
class BadDateFormatException(Exception):
    """ Raised by MovieTopAPIView when date has a wrong format """


class CommentAPIView(CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = Comment.objects.all()
    
    def get(self, request):
        self.serializer_class = CommentListSerializer
        return self.list(request)
    
    def get_queryset(self):
        """ Enables getting comments by movie id """
        movie_id = self.request.GET.get('movie')
        if movie_id:
            return super().get_queryset().filter(object_id=movie_id)
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        self.serializer_class = CommentCreateSerializer
        return self.create(request, args, kwargs)

    def perform_create(self, serializer):
        movie_id = self.request.POST.get('movie_id')
        content_type = ContentType.objects.get_for_model(Movie)
        serializer.save(content_type=content_type, object_id=movie_id)


class MovieAPIView(CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    
    def get(self, request):
        return self.list(request)
    
    def get_queryset(self):
        """ Enable getting movies by genre or/and director """
        genre = self.request.GET.get('genre')
        director = self.request.GET.get('director')
        queryset = super().get_queryset()
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if director:
            queryset = queryset.filter(director__icontains=director)
        return queryset
    
    def post(self, request):
        title = request.POST.get('title')
        query_result = Movie.objects.filter(title__icontains=title)
        # check if movie with this title already exists in the PostgreSQL database:
        if query_result.exists():
            movie_obj = query_result.first()
            serializer = MovieDetailSerializer(movie_obj)
            return Response(serializer.data)
        # if not, get it from the omdbapi:
        else:
            movie_data = fetch_movie(title)
            if movie_data['response'] == 'True' and movie_data['type'] == 'movie':
                movie_data['ratings'] = json.dumps(movie_data['ratings'])
                movie_obj = Movie.objects.create(**movie_data)
                serializer = MovieDetailSerializer(movie_obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)


class MovieDeleteUpdateAPIView(DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, **kwargs)


class MovieTopAPIView(ListAPIView):
    """
    Top movies present in the database based
    on a number of comments in a certain date range.
    The view requires query string as parameters 'from' and 'to'.
    If one of the parameters is missing, displays error with message
    about what parameters should be passed.
    If the date format is different from 'YYYY-MM-DD', displays error
    message with information what proper date format should be.
    
    As there wasn't specified whether movies without comments
    in a certain date range should be displayed, I decided
    to display them with number of comments = 0 (last positions).
    """
    serializer_class = MovieRankSerializer

    def get_queryset(self):
        """
        Window function 'DenseRank' used to provide
        rank values with desired behaviour.
        Raising custom exceptions enables 'get()' function
        to return proper error messages.
        """
        date_from = self.request.GET.get('from')
        date_to = self.request.GET.get('to')
        if not date_from or not date_to:
            raise NoDateRangeException()
        window = Window(expression=DenseRank(), order_by=F('comment_count').desc())
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            raise BadDateFormatException()
        queryset = Movie.objects.annotate(
            comment_count=Count('comments',
                                filter=Q(comments__created__date__range=(date_from, date_to))),
            rank=window)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Catch custom exceptions raised by 'get_queryset()'
        to return results or proper error message.
        """
        try:
            response = self.list(request, *args, **kwargs)
        except NoDateRangeException:
            return Response({
                "error": "No date range specified. "
                         "The query must include both 'from' and 'to' parameters specified."},
                status=status.HTTP_400_BAD_REQUEST)
        except BadDateFormatException:
            return Response({
                "error": "Invalid date format. The right format is 'YYYY-MM-DD'."},
                status=status.HTTP_400_BAD_REQUEST)
        return response
