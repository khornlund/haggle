

class SessionBase:
    """Interface for managing a buy/sell session"""

    def start(self):
        raise NotImplementedError('You must implement this method!')

    def receive(self, m):
        raise NotImplementedError('You must implement this method!')


class SessionBuy(SessionBase):

    def __init__(self, item):
        self._item = item

    def start(self):
        return f'Hello I am looking to buy {self._item}'

    def recieve(self, m):
        return f'I understand. How about X?'


class SessionSell(SessionBase):

    def __init__(self, item):
        self._item = item

    def start(self):
        return f'Hello I am looking to sell {self._item}'

    def recieve(self, m):
        return f'I understand. How about X?'
