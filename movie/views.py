
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page</h1>')
    #return render(request,'home.html')
    #return render(request,'home.html',{'name':'Juan Restrepo Higuita'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm, 'movies':movies})

def about(request):
    #return HttpResponse('<h1>About</h1>')
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html',{'email':email})

def statistics_view(request):
    matplotlib.use('Agg')

    plt.figure()  # Crea una nueva figura

    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        genre = movie.genre.split(', ')[0] if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1


    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    #Creating the first graphic
    plt.bar(bar_positions, movie_counts_by_year.values(),width=bar_width, align="center")
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    #Saving the first image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    #Creating the second graphic
    plt.figure()  # Crea otra nueva figura para la segunda gráfica
    bar2_positions = range(len(movie_counts_by_genre))

    plt.bar(bar2_positions, movie_counts_by_genre.values(),width=bar_width, align="center")
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar2_positions, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    
    #Saving the second image
    buffer_2 = io.BytesIO()
    plt.savefig(buffer_2, format='png')
    buffer_2.seek(0)
    plt.close

    another_image_png = buffer_2.getvalue()
    buffer_2.close()
    graphic_2 = base64.b64encode(another_image_png)
    graphic_2 = graphic_2.decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic,'graphic_2': graphic_2})
