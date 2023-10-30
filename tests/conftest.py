import pytest
import responses

from gistapi.gistapi import app


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def testapp():
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(testapp):
    return testapp.test_client()


@pytest.fixture
def sample_gist_file_content():
    return """
    def read_line_by_line():
        with open("loadme.csv", "r") as f:
            for row in f:
                yield row

    match http_status:
        case 200 | 201 | 204 as status:
            print(f"Ok! {status = }")
        case 400 | 404 as status:
            print(f"You did something wrong! {status = }")
        case 500 as status:
            print(f"Something went wrong! {status = }")
        case _ as status:
            print(f"Unexpected {status = }!")
    """
