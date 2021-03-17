import requests
from django.shortcuts import render, redirect

from utils import global_variables
from utils.utility_classes import NirvanaLogger
from utils.utility_classes import Spotify, SpotifyResult, SpotifyPlaylist

logger = NirvanaLogger(__name__)


def search(request):
    try:
        if request.method == 'POST':
            search_text = request.POST['search_text']
            search_type = request.POST['search_type']
            url = global_variables.SPOTIFY_SEARCH_URL.format(
                search_text, search_type)
            spotify_obj = Spotify()
            headers = spotify_obj.get_headers()
            r = requests.get(url=url, headers=headers)
            d = r.json()
            search_type += 's'
            n = len(d[search_type]['items'])
            search_result = []
            for i in range(n):
                name = d[search_type]['items'][i]['name']
                url = d[search_type]['items'][i]['external_urls']['spotify']
                search_result.append(SpotifyResult(name, url))
            return render(request, 'search.html', {'search_result': search_result, 'title': 'Spotify'})
    except Exception as ex:
        logger.write_to_console(str(ex), ' spotify search')
        request.session['message'] = str(ex)
        return redirect('error')


def categories(request):
    try:
        spotify_obj = Spotify()
        headers = spotify_obj.get_headers()
        r = requests.get(url=global_variables.SPOTIFY_CATEGORIES_URL, headers=headers)
        d = r.json()
        n = len(d['categories']['items'])
        categories_list = []
        for i in range(n):
            cat_name = d['categories']['items'][i]['name']
            cat_id = d['categories']['items'][i]['id']
            cat_url = global_variables.SPOTIFY_PLAYLIST_URL.format(
                cat_id)
            categories_list.append(SpotifyResult(cat_name, cat_url))
        data = {'categories': categories_list, 'title': 'Spotify'}
        return render(request, 'categories.html', data)
    except Exception as ex:
        logger.write_to_console(str(ex), 'spotify cetegories')
        request.session['message'] = str(ex)
        return redirect('error')


def playlists(request, url):
    try:
        url = url.replace('+', '/')
        spotify_obj = Spotify()
        headers = spotify_obj.get_headers()
        r = requests.get(url=url, headers=headers)
        playlistss = r.json()
        items = []
        if 'playlists' in playlistss:
            m = len(playlistss['playlists']['items'])
            if m > 0:
                for j in range(m):
                    playlist = playlistss['playlists']['items'][j]
                    name = playlist['name']
                    url = playlist['external_urls']['spotify']
                    image = playlist['images'][0]['url']
                    items.append(SpotifyPlaylist(name, url, image))
        data = {'items': items, 'title': 'Spotify'}
        return render(request, 'playlists.html', data)
    except Exception as ex:
        logger.write_to_console(str(ex), 'spotify playlists')
        request.session['message'] = str(ex)
        return redirect('error')


def player(request, url):
    try:
        url = url.replace('+', '/').replace('.com/', '.com/embed/')
        return render(request, 'player.html', {'url': url, 'title': 'Spotify'})
    except Exception as ex:
        logger.write_to_console(str(ex), 'spotify player')
        request.session['message'] = str(ex)
        return redirect('error')
