import time

from elasticsearch import Elasticsearch, exceptions

from haggle.logger import setup_logger


class ElasticHandler:
    """Manages posting to/searching the elasticsearch database"""

    DOC_TYPE = 'chat-message'

    def __init__(self, host='es'):
        self.logger = setup_logger(self.__class__.__name__)
        self.logger.debug(f'Initialising connection to "{host}"')
        self._es = Elasticsearch(host=host)
        self.logger.debug(f'Connected to "{host}"')

    def post(self, index, chat_message):
        """Post a chat message to the elasticsearch database"""
        self._es.index(
            index=index,
            doc_type=self.DOC_TYPE,
            body=chat_message
        )

    def search(self, index):
        """Search the elasticsearch database for chat messages"""
        if self.safe_check_index(index):
            return self._es.search(index=index, doc_type=self.DOC_TYPE)
        else:
            self.logger.warning(f'Index "{index}" does not exist!')
            return None

    def safe_check_index(self, index, retry=3):
        """Connect to ES with retry"""
        if not retry:
            self.logger.warning('Out of retries. Bailing out...')
            return False
        try:
            status = self._es.indices.exists(index)
            return status
        except exceptions.ConnectionError as ex:  # noqa
            self.logger.warning('Unable to connect to ES. Retrying in 5 secs...')
            time.sleep(5)
            self.safe_check_index(index, retry - 1)


class ElasticIndices:
    """Enum for elasticsearch indices"""

    HUMAN_BUYER = 'human-buyer'
    HUMAN_SELLER = 'human-seller'
