import re
import urllib
import urllib.request
import uuid

import bs4

import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">$119.99</span>
        data = dict()
        data[
            'User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        request = urllib.request.Request(self.url, headers=data)
        content = urllib.request.urlopen(request)
        soup = bs4.BeautifulSoup(content, 'html.parser')
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile('(\d+.\d+)')
        match = pattern.search(string_price)

        self.price = float(match.group().replace(',', ''))

        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())
        pass

    def json(self):
        return {
            'name': self.name,
            'url': self.url,
            '_id': self._id,
            'price': self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        data = Database.find_one(ItemConstants.COLLECTION, {"_id": item_id})
        return cls(**data)
