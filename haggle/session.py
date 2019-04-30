import abc
import datetime
from uuid import uuid4

from model import ModelBuyer, ModelSeller


class ChatMessage:

    TIMESTAMP = 'timestamp'
    IS_HUMAN = 'is_human'
    ROLE = 'role'
    MESSAGE = 'message'

    @classmethod
    def create(cls, is_human, role, m):
        return {
            cls.TIMESTAMP: datetime.datetime.now(),
            cls.IS_HUMAN: is_human,
            cls.ROLE: role,
            cls.MESSAGE: m
        }


class SessionBase(abc.ABC):

    timeout_timedelta = datetime.timedelta(seconds=10 * 60)  # 10 minutes

    def __init__(self):
        self._uuid = str(uuid4())
        self._model = self.model_factory()
        self._timestamp()
        self._chatlog = []

    @property
    def uuid(self):
        return self._uuid

    def receive(self, m):
        self._timestamp()

        if self.is_human_buyer:
            self._log_buyer_msg(m)
        else:
            self._log_seller_msg(m)

        resp = self._model.receive(m)

        if self.is_human_buyer:
            self._log_seller_msg(resp)
        else:
            self._log_buyer_msg(resp)

        return resp

    def _log_buyer_msg(self, m):
        self._log_msg(self.is_human_buyer, 'buyer', m)

    def _log_seller_msg(self, m):
        self._log_msg(self.is_human_seller, 'seller', m)

    def _log_msg(self, is_human, role, m):
        self._chatlog.append(ChatMessage.create(is_human, role, m))

    def _timestamp(self):
        self._last_time = datetime.datetime.now()

    def is_expired(self):
        return (datetime.datetime.now() - self._last_time) > self.timeout_timedelta

    @property
    def data(self):
        return {
            'type': self.__class__.__name__,
            'last': self._last_time.strftime('%Y-%m-%d %H:%M:%S'),
            'log': self._chatlog
        }

    @abc.abstractmethod
    def model_factory(self):
        pass

    @property
    @abc.abstractmethod
    def is_human_buyer(self):
        pass

    @property
    @abc.abstractmethod
    def is_human_seller(self):
        pass


class SessionHumanBuyer(SessionBase):

    def __init__(self):
        super(SessionHumanBuyer, self).__init__()

    @property
    def is_human_buyer(self):
        return True

    @property
    def is_human_seller(self):
        return False

    def model_factory(self):
        return ModelBuyer('Car')


class SessionHumanSeller(SessionBase):

    def __init__(self):
        super(SessionHumanSeller, self).__init__()

    @property
    def is_human_buyer(self):
        return False

    @property
    def is_human_seller(self):
        return True

    def model_factory(self):
        return ModelSeller('House')


class SessionManager:

    buyers = {}
    sellers = {}

    def new_buyer(self):
        self.cleanup()
        buyer = SessionHumanBuyer()
        self.buyers[buyer.uuid] = buyer
        return buyer

    def new_seller(self):
        self.cleanup()
        seller = SessionHumanSeller()
        self.sellers[seller.uuid] = seller
        return seller

    def cleanup(self):
        for k, v in self.buyers.items():
            if v.is_expired():
                del self.buyers[k]

        for k, v in self.sellers.items():
            if v.is_expired():
                del self.sellers[k]
