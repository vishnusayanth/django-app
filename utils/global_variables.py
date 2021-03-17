import os

from locations.models import State, Continent

EMAIL = os.environ['EMAIL']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
SMTP_SERVER = os.environ['SMTP_SERVER']
SMTP_PORT = '587'

NEWS_URL_TO_SCRAPE = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE55YXpBU0FtVnVLQUFQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
NEWS_MAIN_DIV_CLASS = 'lBwEZb BL5WZb GndZbb'
NEWS_SUB_DIV_CLASS = 'xrnccd F6Welf R7GTQ keNKEd j7vNaf'
NEWS_HEADLINE_CLASS = 'DY5T1d RZIKme'
NEWS_IMAGE_CLASS = 'tvs3Id QwxBBf'
NEWS_LINK_CLASS = 'FKF6mc TpQm9d ZqhUjb ztUP4e tHCKTc kTeh9 cd29Sd dHeVVb lSLCF Xcw0p'
NEWS_LINK = 'https://news.google.com/'

LINKEDIN_URL = 'https://www.linkedin.com/in/'

ZOMATO_IFRAME_URL = 'https://www.zomato.com/widgets/res_search_widget.php?city_id=11772&language_id=1&theme=red&widgetType=large&sort=rating'

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search?q={0}&type={1}'
SPOTIFY_CATEGORIES_URL = 'https://api.spotify.com/v1/browse/categories'
SPOTIFY_PLAYLIST_URL = 'https://api.spotify.com/v1/browse/categories/{0}/playlists'

PASSWORD_COMPLEXITY = '''
    Your password must contain 7 characters, an alphabet and a number.
'''


def GET_STATES():
    return State.objects.all().values_list('name', flat=True).order_by('name')


def GET_CONTINENTS():
    return Continent.objects.all().values_list('name', flat=True).order_by('name')


email_frame = '''
<body style="font-family: Arial, Helvetica, sans-serif;">
  <div style="padding: 20px;background-color: #f1f1f1;">
    <h2>New message from a visitor!</h2>
    <p></p>
    <p>{0}</p>
    <p></p>
  </div>
</body>
'''
