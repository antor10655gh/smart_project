from django.shortcuts import render
from django.http import HttpResponse
from smart_app.models import Musician, Album
from smart_app import forms
from django.db.models import Avg

# Create your views here.
def home(request):
    musician_list = Musician.objects.order_by('first_name')
    diction = {'title':'home page', 'musician_list':musician_list}
    return render(request, 'smart_app/home.html', context=diction)

def album_list(request, artist_id):
    artist_info   = Musician.objects.get(pk=artist_id)
    album_list    = Album.objects.filter(artist=artist_id).order_by('name')
    artist_rating = Album.objects.filter(artist=artist_id).aggregate(Avg('num_stars'))

    diction = {'title':'list of album','artist_info':artist_info,'album_list':album_list,'artist_rating':artist_rating}
    return render(request, 'smart_app/album_list.html', context=diction)

def musician_form(request):
    m_form  = forms.MusicianForm()

    if request.method == 'POST':
        m_form = forms.MusicianForm(request.POST)

        if m_form.is_valid():
            m_form.save(commit=True)
            return home(request)

    diction = {'title':'add musician', 'm_form':m_form}
    return render(request, 'smart_app/musician_form.html', context=diction)

def album_form(request):
    l_form = forms.AlbumForm()

    if request.method == 'POST':
        l_form = forms.AlbumForm(request.POST)

        if l_form.is_valid():
            l_form.save(commit=True)
            return home(request)
    diction = {'title':'add album', 'l_form':l_form}
    return render(request, 'smart_app/album_form.html', context=diction)

def edit_artist(request, artist_id):
    artist_info   = Musician.objects.get(pk=artist_id)
    edit_form  = forms.MusicianForm(instance=artist_info)

    if request.method == 'POST':
        edit_form = forms.MusicianForm(request.POST, instance=artist_info)

        if edit_form.is_valid():
            edit_form.save(commit=True)
            return album_list(request, artist_id)


    diction = {'edit_form':edit_form,}
    return render(request, 'smart_app/edit_artist.html', context=diction)

def edit_album(request, album_id):
    album_info = Album.objects.get(pk=album_id)
    edit_form  = forms.AlbumForm(instance = album_info)
    diction = {}
    if request.method == 'POST':
        edit_form = forms.AlbumForm(request.POST, instance = album_info)

        if edit_form.is_valid():
            edit_form.save(commit=True)
            diction.update({'success_sms':'Successfully Updated'})


    diction.update({'edit_form':edit_form})
    diction.update({'album_id':album_id})
    return render(request, 'smart_app/edit_album.html', context=diction)

def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id).delete()
    diction = {'delete_sucess':'Successfully Deleted!'}
    return render(request, 'smart_app/delete.html', context=diction)
