from requests import Response
from http import HTTPStatus

class ResponseSpecs:
    @staticmethod
    def status_code_200():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def status_code_201():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def status_code_400():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def status_code_401():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    @staticmethod
    def status_code_403():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text

        return confirm

    @staticmethod
    def status_code_404():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text

        return confirm

    @staticmethod
    def status_code_422():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text

        return confirm
