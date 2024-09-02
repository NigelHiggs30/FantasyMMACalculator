from bs4 import BeautifulSoup
from typing import List

def url_links(soup: BeautifulSoup) -> List[str]:
    
    rows = soup.find_all("tr",class_="b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
    urls = []
    for row in rows:
        data_link = row.get('data-link')
        if data_link:
            urls.append(data_link)

    return urls

