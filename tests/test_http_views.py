import pytest

from bocadillo import App, view
from bocadillo.constants import ALL_HTTP_METHODS


def test_can_register_class_based_view(app: App):
    @app.route("/")
    class Index:
        pass


@pytest.mark.parametrize("method", map(str.lower, ALL_HTTP_METHODS))
def test_if_method_not_implemented_then_405(app: App, method: str):
    @app.route("/")
    class Index:
        pass

    response = getattr(app.client, method)("/")
    assert response.status_code == 405


def test_if_method_implemented_then_as_normal(app: App):
    @app.route("/")
    class Index:
        async def get(self, req, res):
            res.text = "Get!"

    response = app.client.get("/")
    assert response.status_code == 200
    assert response.text == "Get!"


def test_if_handle_is_implemented_then_bypasses_other_methods(app: App):
    @app.route("/")
    class Index:
        async def handle(self, req, res):
            res.text = "Handle!"

        async def get(self, req, res):
            res.text = "Get!"

    response = app.client.get("/")
    assert response.status_code == 200
    assert response.text == "Handle!"


def test_sync_handler(app: App):
    @app.route("/")
    class Index:
        def get(self, req, res):
            pass

    assert app.client.get("/").status_code == 200


def test_function_based(app: App):
    @app.route("/")
    @view()
    def index(req, res):
        pass

    assert app.client.get("/").status_code == 200


def test_view_decorator_is_optional(app: App):
    @app.route("/")
    def index(req, res):
        pass

    assert app.client.get("/").status_code == 200


def test_from_obj(app: App):
    class MyView:
        async def get(self, req, res):
            pass

    app.route("/")(MyView())
    assert app.client.get("/").status_code == 200
