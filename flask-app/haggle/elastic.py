from elasticsearch import Elasticsearch


class ElasticHandler:
    """Manages posting to/searching the elasticsearch database"""

    DOC_TYPE = 'chat-message'

    def __init__(self, host='es'):
        self._es = Elasticsearch(host=host)

    def post(self, index, chat_message):
        """Post a chat message to the elasticsearch database"""
        self._es.index(
            index=index,
            doc_type=self.DOC_TYPE,
            body=chat_message
        )

    def search(self, index):
        """Search the elasticsearch database for chat messages"""
        return self._es.search(index=index, doc_type=self.DOC_TYPE)


class ElasticIndices:
    """Enum for elasticsearch indices"""

    HUMAN_BUYER = 'human-buyer'
    HUMAN_SELLER = 'human-seller'
