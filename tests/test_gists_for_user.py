import pytest
import responses

from gistapi.gistapi import Gist, GistFile, UserNotFound, gists_for_user
from tests import factories as fty


@pytest.mark.parametrize(
    "user_gists",
    [
        pytest.param([], id="no gists"),
        pytest.param(fty.GHGistFactory.create_batch(3), id="some gists"),
    ],
)
def test_returns_gists(mocked_responses, user_gists):
    username = "foobar"
    url = f"https://api.github.com/users/{username}/gists"
    mocked_responses.add(responses.GET, url, json=user_gists)
    result = gists_for_user(username)
    assert isinstance(result, list)
    if user_gists:
        assert len(result)
        assert all(isinstance(o, Gist) for o in result)
        assert all(len(o.files) and all(isinstance(f, GistFile) for f in o.files) for o in result)
    else:
        assert result == []


def test_raises_error_for_user_not_found(mocked_responses):
    username = "foobar"
    url = f"https://api.github.com/users/{username}/gists"
    mocked_responses.add(responses.GET, url, status=404)
    with pytest.raises(UserNotFound):
        gists_for_user(username)
