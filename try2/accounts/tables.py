import django_tables2 as tables
from .models import Album, Review, Aoty

class AlbumTable(tables.Table):
    class Meta:
        model = Album
        template_name = "django_tables2/bootstrap4.html"
        fields = ("artist", "title", "release_date", "format", "label", "genre",)

class ReviewTable(tables.Table):
    class Meta:
        model = Review
        template_name = "django_tables2/bootstrap4.html"
        fields = ("album", "metacritic_critic_score", "metacritic_reviews", "metacritic_user_score", "metacritic_user_reviews")

class AotyTable(tables.Table):
    class Meta:
        model = Aoty
        template_name = "django_tables2/bootstrap4.html"
        fields = ("album", "aoty_critic_score", "aoty_critic_reviews", "aoty_user_score", "aoty_user_reviews")
