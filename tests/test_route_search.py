from typing import cast

import pytest
import responses

from tests import factories as fty


@pytest.mark.parametrize(
    "pattern,does_match",
    [
        pytest.param("barbaz", False),
        pytest.param(r"\s*match http_status", True),
    ],
)
def test_returns_200(client, sample_gist_file_content, mocked_responses, pattern, does_match):
    username = "foobar"
    gist = cast(dict, fty.GHGistFactory(filenames=["something.py"]))
    mocked_responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        json=[gist],
    )
    mocked_responses.add(
        responses.GET,
        next(iter(gist["files"].values()))["raw_url"],
        body=sample_gist_file_content,
    )
    payload = {"username": username, "pattern": pattern}
    response = client.post("/api/v1/search", json=payload)
    assert response.status_code == 200
    assert len(response.json["matches"]) == (1 if does_match else 0)


def test_returns_404(client, mocked_responses):
    username = "foobar"
    mocked_responses.add(
        responses.GET,
        f"https://api.github.com/users/{username}/gists",
        status=404,
    )
    payload = {"username": username, "pattern": "any"}
    response = client.post("/api/v1/search", json=payload)
    assert response.status_code == 404
    expected = {
        **payload,
        "status": "failure",
        "error": f"no user found with name {username}",
        "matches": [],
    }
    assert response.json == expected


def test_returns_422(client):
    pattern = "he(lo"
    payload = {"username": "barbaz", "pattern": pattern}
    response = client.post("/api/v1/search", json=payload)
    assert response.status_code == 422
    expected = {
        **payload,
        "status": "failure",
        "error": f"invalid pattern {pattern}: missing ), unterminated subpattern at position 2",
        "matches": [],
    }
    assert response.json == expected
