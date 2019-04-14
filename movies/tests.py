from datetime import datetime
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase

from .models import (
    Comment,
    Movie,
)


matrix_sample = {'title': 'The Matrix', 'year': '1999', 'rated': 'R', 'released': '31 Mar 1999',
                 'runtime': '136 min', 'genre': 'Action, Sci-Fi',
                 'director': 'Lana Wachowski, Lilly Wachowski',
                 'writer': 'Lilly Wachowski, Lana Wachowski',
                 'actors': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving',
                 'plot': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                 'language': 'English', 'country': 'USA',
                 'awards': 'Won 4 Oscars. Another 34 wins & 48 nominations.',
                 'poster': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
                 'ratings': [{'Source': 'Internet Movie Database', 'Value': '8.7/10'},
                             {'Source': 'Rotten Tomatoes', 'Value': '88%'},
                             {'Source': 'Metacritic', 'Value': '73/100'}], 'metascore': '73',
                 'imdbrating': '8.7', 'imdbvotes': '1,488,823', 'imdbid': 'tt0133093',
                 'type': 'movie', 'dvd': '21 Sep 1999', 'boxoffice': 'N/A',
                 'production': 'Warner Bros. Pictures',
                 'website': 'http://www.whatisthematrix.com', 'response': 'True'}

godfather_sample = {'title': 'The Godfather', 'year': '1972', 'rated': 'R',
                    'released': '24 Mar 1972', 'runtime': '175 min', 'genre': 'Crime, Drama',
                    'director': 'Francis Ford Coppola',
                    'writer': 'Mario Puzo (screenplay by), Francis Ford Coppola (screenplay by), Mario Puzo (based on the novel by)',
                    'actors': 'Marlon Brando, Al Pacino, James Caan, Richard S. Castellano',
                    'plot': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                    'language': 'English, Italian, Latin', 'country': 'USA',
                    'awards': 'Won 3 Oscars. Another 24 wins & 28 nominations.',
                    'poster': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
                    'ratings': [{'Source': 'Internet Movie Database', 'Value': '9.2/10'},
                                {'Source': 'Metacritic', 'Value': '100/100'}], 'metascore': '100',
                    'imdbrating': '9.2', 'imdbvotes': '1,417,421', 'imdbid': 'tt0068646',
                    'type': 'movie', 'dvd': '09 Oct 2001', 'boxoffice': 'N/A',
                    'production': 'Paramount Pictures', 'website': 'http://www.thegodfather.com',
                    'response': 'True'}

batman_sample = {'title': 'Batman', 'year': '1989', 'rated': 'PG-13', 'released': '23 Jun 1989',
                'runtime': '126 min', 'genre': 'Action, Adventure', 'director': 'Tim Burton',
                'writer': 'Bob Kane (Batman characters), Sam Hamm (story), Sam Hamm (screenplay), Warren Skaaren (screenplay)',
                'actors': 'Michael Keaton, Jack Nicholson, Kim Basinger, Robert Wuhl',
                'plot': 'The Dark Knight of Gotham City begins his war on crime with his first major enemy being the clownishly homicidal Joker.',
                'language': 'English, French, Spanish', 'country': 'USA, UK',
                'awards': 'Won 1 Oscar. Another 8 wins & 26 nominations.',
                'poster': 'https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg',
                'ratings': [{'Source': 'Internet Movie Database', 'Value': '7.5/10'},
                            {'Source': 'Rotten Tomatoes', 'Value': '71%'},
                            {'Source': 'Metacritic', 'Value': '69/100'}], 'metascore': '69',
                'imdbrating': '7.5', 'imdbvotes': '309,868', 'imdbid': 'tt0096895',
                'type': 'movie', 'dvd': '25 Mar 1997', 'boxoffice': 'N/A',
                'production': 'Warner Bros. Pictures', 'website': 'N/A', 'response': 'True'}


def mock_fetch_movie(title):
    if title == 'Watchmen':
        return {'title': 'Watchmen', 'year': '2009', 'rated': 'R', 'released': '06 Mar 2009',
                'runtime': '162 min', 'genre': 'Action, Drama, Mystery, Sci-Fi',
                'director': 'Zack Snyder',
                'writer': 'David Hayter (screenplay), Alex Tse (screenplay), Dave Gibbons (graphic novel illustrator)',
                'actors': 'Malin Akerman, Billy Crudup, Matthew Goode, Jackie Earle Haley',
                'plot': 'In 1985 where former superheroes exist, the murder of a colleague sends active vigilante Rorschach into his own sprawling investigation, uncovering something that could completely change the course of history as we know it.',
                'language': 'English', 'country': 'USA', 'awards': '11 wins & 22 nominations.',
                'poster': 'https://m.media-amazon.com/images/M/MV5BY2IzNGNiODgtOWYzOS00OTI0LTgxZTUtOTA5OTQ5YmI3NGUzXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
                'ratings': [{'Source': 'Internet Movie Database', 'Value': '7.6/10'},
                            {'Source': 'Rotten Tomatoes', 'Value': '64%'},
                            {'Source': 'Metacritic', 'Value': '56/100'}], 'metascore': '56',
                'imdbrating': '7.6', 'imdbvotes': '451,359', 'imdbid': 'tt0409459',
                'type': 'movie', 'dvd': '21 Jul 2009', 'boxoffice': '$107,453,620',
                'production': 'Warner Bros. Pictures', 'website': 'http://www.watchmenmovie.com/',
                'response': 'True'}


class MovieTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(**matrix_sample)
        Movie.objects.create(**godfather_sample)
        Movie.objects.create(**batman_sample)
        
        # test 'top' view: make 3 comments for 'Batman', 1 comment for 'Godfather'.
        movie = ContentType.objects.get_for_model(Movie)
        Comment.objects.create(text="comment_1", object_id=2, content_type=movie)
        Comment.objects.create(text="comment_2", object_id=3, content_type=movie)
        Comment.objects.create(text="comment_3", object_id=3, content_type=movie)
        Comment.objects.create(text="comment_4", object_id=3, content_type=movie)

    def test_movies_get(self):
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 3)
        
    def test_movies_get_with_filter(self):
        response = self.client.get('/movies?director=burton')
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Batman')
    
    @patch('movies.utils.fetch_movie', mock_fetch_movie)
    def test_movies_post_not_exists(self):
        response = self.client.post('/movies', {'title': 'Watchmen'})
        self.assertEqual(response.status_code, 201)
        created_obj = Movie.objects.last()
        self.assertEqual(created_obj.title, 'Watchmen')
        self.assertEqual(created_obj.id, response.json()['id'])
    
    @patch('movies.utils.fetch_movie', mock_fetch_movie)
    def test_movies_post_already_exists(self):
        response = self.client.post('/movies', {'title': 'The Matrix'})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['title'], 'The Matrix')

    def test_movies_delete(self):
        response = self.client.delete('/movies/1')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Movie.objects.filter(id=1).exists())

    def test_movies_update(self):
        response = self.client.put('/movies/2', {'director': 'Monty Python'})
        self.assertEqual(response.status_code, 200)
        updated_obj = Movie.objects.get(pk=2)
        self.assertEqual(updated_obj.director, 'Monty Python')

    def test_comments_get(self):
        response = self.client.get('/comments')
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEquals(len(results), 4)
        
    def test_comments_get_with_movie_id(self):
        response = self.client.get('/comments?movie=3')
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEquals(len(results), 3)
        for comment in results:
            self.assertEquals(comment['movie_id'], 3)

    def test_comments_post(self):
        response = self.client.post('/comments', {
            'movie_id': 2,
            'text': 'Hello Corleone!'
        })
        self.assertEqual(response.status_code, 201)
        created_obj = Comment.objects.last()
        self.assertEqual(created_obj.text, 'Hello Corleone!')
    
    def test_movies_top(self):
        today = str(datetime.today().date())
        response = self.client.get(f'/top?from={today}&to={today}')
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['title'], 'Batman')
        self.assertEqual(results[0]['rank'], 1)
        self.assertEqual(results[1]['title'], 'The Godfather')
        self.assertEqual(results[1]['rank'], 2)

    def test_movies_top_missing_params(self):
        response = self.client.get('/top')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
                "error": "No date range specified. "
                         "The query must include both 'from' and 'to' parameters specified."
        })
    
    def test_movies_top_bad_date_format(self):
        response = self.client.get('/top?from=2019-99-99&to=2019-99-99')
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
                "error": "Invalid date format. The right format is 'YYYY-MM-DD'."
        })
