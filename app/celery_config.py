from celery import Celery
class MailCelery(Celery):

    def __init__(self, *args, **kwargs):
        self.__has_address = False
        super().__init__(*args, **kwargs)

    def set_addr(self, broker_url: str, result_url: str) -> None:
        self.__set_urls(broker_url, result_url)
        return self.__set_has_address(True)

    def __set_urls(self, broker_url: str, result_url: str) -> None:
        self.conf.broker_url = broker_url
        self.conf.result_backend = result_url

    def __set_has_address(self, b: bool) -> None:
        self.__has_address = b        

    def has_address(self) -> bool:
        return self.__has_address

celery = MailCelery(__name__)
celery.conf.imports = ['app.core.components.mail.controller.mailmanager']
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']


