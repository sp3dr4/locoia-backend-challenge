from typing import cast

import pytest
import responses

from gistapi.gistapi import Gist, InvalidPattern, search_gist
from tests import factories as fty


@pytest.mark.parametrize(
    "pattern,expected",
    [
        pytest.param(r"foobar", False),
        pytest.param(r"\s*with open", True),
        pytest.param(r".*Ok!", True),
        pytest.param(r".*Ok!$", False),
    ],
)
def test_finds_match_for_pattern(mocked_responses, sample_gist_file_content, pattern, expected):
    gist = cast(Gist, fty.GistFactory(files_count=1))
    mocked_responses.add(responses.GET, gist.files[0].raw_url, body=sample_gist_file_content)
    result = search_gist(gist, pattern)
    assert result == expected


def test_raises_for_invalid_pattern():
    with pytest.raises(InvalidPattern):
        search_gist(cast(Gist, fty.GistFactory()), "he(lo")
