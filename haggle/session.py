import abc
import datetime
from uuid import uuid4

from model import ModelBuyer, ModelSeller


class SessionBase(abc.ABC):

    timeout_timedelta = datetime.timedelta(seconds=10 * 60)  # 10 minutes

    def __init__(self):
        self._uuid = str(uuid4())
        self._model = self.model_factory()
        self._timestamp()

    @property
    def uuid(self):
        return self._uuid

    @abc.abstractmethod
    def model_factory(self):
        pass

    def message(self, m):
        self._timestamp()
        return self._model.message(m)

    def _timestamp(self):
        self._last_time = datetime.datetime.now()

    def is_expired(self):
        return (datetime.datetime.now() - self._last_time) > self.timeout_timedelta


class SessionBuyer(SessionBase):

    def __init__(self):
        super(SessionBuyer, self).__init__()

    def model_factory(self):
        return ModelBuyer('Car')


class SessionSeller(SessionBase):

    def __init__(self):
        super(SessionSeller, self).__init__()

    def model_factory(self):
        return ModelSeller('House')


class SessionManager:

    buyers = {}
    sellers = {}

    def new_buyer(self):
        self.cleanup()
        buyer = SessionBuyer()
        self.buyers[buyer.uuid] = buyer
        return buyer.uuid

    def new_seller(self):
        self.cleanup()
        seller = SessionSeller()
        self.sellers[seller.uuid] = seller
        return seller.uuid

    def cleanup(self):
        for k, v in self.buyers.items():
            if v.is_expired():
                del self.buyers[k]

        for k, v in self.sellers.items():
            if v.is_expired():
                del self.sellers[k]
