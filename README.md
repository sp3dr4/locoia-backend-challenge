# Gistapi

First of all, I assumed that the search endpoint expects a fully fledged regular expression.  
I mean that, taking the given example `import request`, it will easily find matches because import statements are usually not indented.  
But if, for example, we want to search for `while True`, we should write the pattern as `\s*while True`, to take into consideration the whitespaces at the start of the line where this statement can be found.

## Stretch goals

- I immediately converted to using Poetry, because I'm accustomed to using it, so it would have allowed me to reuse my usual workflow. Assuming poetry is installed, you can run `make install` to install all the local dependencies
- I then added code quality checks, in the form of _black_, _isort_ and _flake8_. They can all be run executing `make lint`, and they'll also be checked with a commit hook. I didn't set up a CI workflow for the sake of time, but I usually do it, so any pull request wouldn't be merged if there's something wrong in the code standards or with the tests
- The tests, written with pytest, can be executed with `make test`
- The service can be run locally by `make run`. Otherwise it can be run in a docker container using `make docker-run`; this will build the image and run it in detached mode, exposing the 9876 port
