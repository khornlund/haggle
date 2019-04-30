import abc


class ModelBase(abc.ABC):
    """Interface for managing a buy/sell session"""

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def receive(self, m):
        pass


class ModelBuyer(ModelBase):

    def __init__(self, item):
        super(ModelBuyer, self).__init__()
        self._item = item

    def start(self):
        return f'Hello I am looking to buy {self._item}'

    def receive(self, m):
        return f'I understand. Would you sell it for X?'


class ModelSeller(ModelBase):

    def __init__(self, item):
        super(ModelSeller, self).__init__()
        self._item = item

    def start(self):
        return f'Hello I am looking to sell {self._item}'

    def receive(self, m):
        return f'I understand. Would you pay X?'
