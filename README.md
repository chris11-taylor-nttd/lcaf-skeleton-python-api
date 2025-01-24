# lcaf-skeleton-python-api

## Overview

This repository contains a reference Python API utilizing FastAPI. Use this skeleton when you want to create an API that can be utilized by other services.

### Features

- Modern package and environment management with `uv`
- Automatic release drafting based on merged pull requests
- Automatic version bumps, tags, and publish to PyPI on release -- simply set your draft to published
- Automatic container build and publish to the GitHub Container Registry (ghcr.io)
- Integrated testing with `pytest`:
    - Sensible default `pytest` configurations
    - Pre-commit hooks to trigger tests before pushing
    - Code coverage checking
    - GitHub workflow
- Recommended plugins file for VSCode

## How to use this repository

### Prerequisites

- [asdf](https://github.com/asdf-vm/asdf) or [mise](https://mise.jdx.dev/) to manage dependencies
- [make](https://www.gnu.org/software/make/)

> NOTE: The workflows in this repository are designed around the target repository being publicly visible. These workflows will require adjustments to work with a private or internal repository.

### Applying the Template

The easiest way to get started is to click the **Use this template** button from the GitHub code page and select **Create a new repository**. Choose the owner of the new repository and give it a name and description.

Alternately, you can consume this template by starting the New Repository workflow and selecting this repository from the **Repository template** dropdown.

Either method will result in GitHub copying the contents of this repository into a new repository for you. Newly-templated repositories receive all the default configurations you'd expect with a new repository, so you may need to set up collaborators and group permissions, enable or disable certain merge types, or tweak other repository settings as needed.

### Post-Template Setup

1. Clone this repository to a machine that meets the [prerequisites](#prerequisites).

2. Run `asdf install` (or `mise install`) to install any needed dependencies on your system.

3. Run `make configure` to download the Launch platform components and initialize the pre-commit hooks.

4. Run `uv sync` to synchronize dependencies declared in `pyproject.toml` to your local machine.

5. Update the contents of `CODEOWNERS` with the individuals or team that will be responsible for providing approvals.

6. Update the contents of `pyproject.toml` with the appropriate values for your project. At a minimum, you should be updating the following fields:

- project.name (be sure you adhere to [PEP-423](https://peps.python.org/pep-0423/)'s naming standards)
- project.description

7. Replace README.md contents with your desired verbiage. README.md is published to PyPI and should reflect your module's information rather than this template information.

### Running your code

Using `uv run` to launch your code ensures that your code runs in an isolated environment. For more information about using `uv run`, see the [official documentation](https://docs.astral.sh/uv/concepts/projects/run/).

Start the FastAPI development server using `uv run fastapi dev src/app.py` (or replace the path with your entrypoint). This enables hot reloads on file save and sends server logs to your terminal for ease of development. For a production-like experience, you can either build and run the container created by the Dockerfile, or issue `uv run uvicorn src.app:app`.

### Building and running local containers

To build a container on your local machine for testing purposes, the following command can be issued:

```sh
# Replace `lcaf-skeleton-python-api` in the commands below with your desired container name
docker buildx build -t lcaf-skeleton-python-api --file ./Dockerfile . --load
```

To run that same container on your local machine and expose the API over port 8000, the following command can be issued:

```sh
# Replace `lcaf-skeleton-python-api` with the container name that you built in the command above.
docker run --rm -ti -p 8000:8000 lcaf-skeleton-python-api
```

This will launch uvicorn with the default settings and start serving your API. You may wish to validate the API is accessible from the host machine by making a request to the healthz endpoint, below is that command and the expected output:

```
$ curl -v http://localhost:8000/healthz
* Host localhost:8000 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8000...
* Connected to localhost (::1) port 8000
> GET /healthz HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.6.0
> Accept: */*
>
< HTTP/1.1 200 OK
< date: Fri, 24 Jan 2025 18:37:44 GMT
< server: uvicorn
< content-length: 0
<
* Connection #0 to host localhost left intact
```

### Running tests

This repository comes with a default configuration for pytest.

To execute tests with the project's dependencies, issue the `uv run pytest` command. You may use the `pytest` command directly only if you activate a virtual environment.

After you have run `make configure` during the initial setup, two targets are available as shortcuts:

- `make test` will run `uvx run pytest`
- `make coverage` will run `make test`, generate coverage reports, and then open the HTML version of the coverage report in a browser for ease of use.

## Further reading

- [Set up VSCode](./docs/ide-vscode.md) for an improved development experience
- [Set up PyPI](./docs/pypi-configuration.md) for package distribution
- Learn how the [release workflows](./docs/release-workflow.md) operate
- [Get started with FastAPI](https://fastapi.tiangolo.com/tutorial/)
- Learn about [uvicorn](https://www.uvicorn.org/), a production-ready ASGI server
