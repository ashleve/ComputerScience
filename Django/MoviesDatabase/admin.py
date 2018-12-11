from django.contrib import admin
from MoviesDatabase.models import Movie, Actor, MovieCast


class MovieCastInline(admin.TabularInline):
    model = MovieCast
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'genre', 'rating', 'num_of_ratings']
	search_fields = ['title', 'genre', 'rating']
	inlines = [
		MovieCastInline,
	]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'surname', 'age', 'gender']
	search_fields = ['name', 'surname', 'age', 'gender']
	inlines = [
		MovieCastInline,
	]
	

@admin.register(MovieCast)
class MovieCastAdmin(admin.ModelAdmin):
	list_display = ['id', 'movie', 'actor', 'role']
	
