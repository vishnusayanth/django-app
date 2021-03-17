from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from utils import global_variables
from utils.utility_classes import GoogleNewsContent
from utils.utility_classes import NirvanaLogger

logger = NirvanaLogger(__name__)


def fetch_news(request):
    try:
        url = global_variables.NEWS_URL_TO_SCRAPE
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', attrs={'class': global_variables.NEWS_MAIN_DIV_CLASS})
        items = []
        for row in table.find_all('div', attrs={'class': global_variables.NEWS_SUB_DIV_CLASS}):
            content = str(row.find('a', attrs={'class': global_variables.NEWS_HEADLINE_CLASS})).split('>')[1].split('<')[0]
            image = str(row.find('img', attrs={'class': global_variables.NEWS_IMAGE_CLASS}))
            link = row.find('a', attrs={'class': global_variables.NEWS_LINK_CLASS})
            link = global_variables.NEWS_LINK + link['href']
            obj = GoogleNewsContent(content, link, image)
            items.append(obj.tojson())
        data = {'data': items}
        return JsonResponse(data)
    except Exception as ex:
        logger.write_to_console(str(ex), 'fetch google news.')
        request.session['message'] = str(ex)
        return None
