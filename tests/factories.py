import factory

from gistapi.gistapi import Gist, GistFile


class GHGistFileFactory(factory.Factory):
    filename = factory.Faker("file_name", category="text")
    type = factory.Faker("mime_type", category="text")
    language = factory.Faker("random_element", elements=["Markdown", "Python", "Text"])
    raw_url = factory.Faker("url")
    size = factory.Faker("numerify", text="##")

    class Meta:
        model = dict


class GHGistFactory(factory.Factory):
    url = factory.Faker("url")
    id = factory.Faker("uuid4")
    html_url = factory.Faker("url")
    files = factory.LazyAttribute(
        lambda o: {name: GHGistFileFactory(filename=name) for name in o.filenames}
    )
    created_at = factory.Faker("iso8601")
    updated_at = factory.Faker("iso8601")
    description = factory.Faker("sentence", nb_words=20)

    class Params:
        filenames = ["foo.md", "bar.py"]

    class Meta:
        model = dict


class GistFileFactory(factory.Factory):
    filename = factory.Faker("file_name", category="text")
    language = factory.Faker("random_element", elements=["Markdown", "Python", "Text"])
    raw_url = factory.Faker("url")

    class Meta:
        model = GistFile


class GistFactory(factory.Factory):
    id = factory.Faker("uuid4")
    html_url = factory.Faker("url")
    files = factory.LazyAttribute(lambda o: GistFileFactory.create_batch(o.files_count))
    created_at = factory.Faker("iso8601")
    updated_at = factory.Faker("iso8601")
    description = factory.Faker("sentence", nb_words=20)

    class Params:
        files_count = 2

    class Meta:
        model = Gist
