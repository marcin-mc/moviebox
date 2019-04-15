from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)


class Comment(models.Model):
    """
    For the purpose of this task comments could be
    implemented using just 'standard' ForeignKey.
    However, I decided to use contenttypes,
    what enables us to add possible new models
    in the future. (e.g. Series).
    """
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Movie(models.Model):
    """
    Since we don't have information on size of fields
    returned from the outer db, it seems a good idea
    to use TextField instead of making assumptions on data size
    and limit entries in our tables using CharField.
    
    I decided to make field 'ratings' JSON serialized,
    as we don't use this field in our project.
    If needed in possible GUI,
    those values could be deserialized in JavaScript.
    """
    title = models.TextField()
    year = models.TextField()
    rated = models.TextField()
    released = models.TextField()
    runtime = models.TextField()
    genre = models.TextField()
    director = models.TextField()
    writer = models.TextField()
    actors = models.TextField()
    plot = models.TextField()
    language = models.TextField()
    country = models.TextField()
    awards = models.TextField()
    poster = models.TextField()
    ratings = models.TextField()
    metascore = models.TextField()
    imdbrating = models.TextField()
    imdbvotes = models.TextField()
    imdbid = models.TextField()
    type = models.TextField()
    dvd = models.TextField()
    boxoffice = models.TextField()
    production = models.TextField()
    website = models.TextField()
    response = models.TextField()
    comments = GenericRelation(Comment, related_query_name='movies')
