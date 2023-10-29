"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""
import inspect
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Self

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


class DataclassBuilder:
    @classmethod
    def from_dict(cls, o: dict) -> Self:
        return cls(**{k: v for k, v in o.items() if k in inspect.signature(cls).parameters})


@dataclass
class GistFile(DataclassBuilder):
    filename: str
    language: str
    raw_url: str


@dataclass
class Gist(DataclassBuilder):
    id: str
    html_url: str
    files: list[GistFile]
    created_at: datetime
    updated_at: datetime | None = None
    description: str | None = None

    def __post_init__(self):
        if self.created_at and isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if self.updated_at and isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


def gists_for_user(username: str) -> list[Gist]:
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = f"https://api.github.com/users/{username}/gists"
    response = requests.get(gists_url)
    gists: list[Gist] = []
    for x in response.json():
        files = [GistFile.from_dict(v) for v in x["files"].values()]
        gist = Gist.from_dict(x | {"files": files})
        gists.append(gist)
    return gists


def search_gist(gist: Gist, pattern: re.Pattern) -> bool:
    for file in gist.files:
        with requests.get(file.raw_url, stream=True) as r:
            if r.encoding is None:
                r.encoding = "utf-8"
            for line in r.iter_lines(decode_unicode=True):
                if line and pattern.match(line):
                    return True
    return False


@app.route("/api/v1/search", methods=["POST"])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()

    username = post_data["username"]
    pattern = post_data["pattern"]
    compiled = re.compile(pattern)

    result = {}
    gists = gists_for_user(username)

    matches = []
    for gist in gists:
        if search_gist(gist, compiled):
            matches.append(asdict(gist))

    result["status"] = "success"
    result["username"] = username
    result["pattern"] = pattern
    result["matches"] = matches

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
