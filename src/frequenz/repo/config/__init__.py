# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

r"""Frequenz project setup tools and common configuration.

The tools are provided to configure the main types of repositories most commonly used at
Frequenz, defined in
[`freq.repo.config.RepositoryType`][freq.repo.config.RepositoryType].

- actor: SDK actors
- api: gRPC APIs
- app: SDK applications
- lib: General purpose Python libraries
- model: SDK machine learning models

# Common

## `nox`

### Writing the `noxfile.py`

Projects wanting to use `nox` to run lint checkers and other utilities can use
the [`frequenz.repo.config.nox`][] package.

When writing the `noxfile.py` you should import the `nox` module from this
package and use the [`frequenz.repo.config.nox.configure`][] function,
which will configure all nox sessions.

You should call `configure()` using one of the default configurations provided
in the [`frequenz.repo.config.nox.default`][] module. For example:

```python
from frequenz.repo.config import nox

nox.configure(nox.default.lib_config)
```

Again, make sure to pick the correct default configuration based on the type of your
project (`actor_config`, `api_config`, `app_config`, `lib_config`, `model_config`).

If you need to modify the configuration, you can copy one of the default
configurations by using the
[`copy()`][frequenz.repo.config.nox.config.Config.copy] method:

```python
from frequenz.repo.config import nox

config = nox.default.lib_config.copy()
config.opts.black.append("--diff")
nox.configure(config)
```

If you need further customization or to define new sessions, you can use the
following modules:

- [`frequenz.repo.config.nox.config`][]: Low-level utilities to configure nox
  sessions. It defines the `Config` and CommandsOptions` classes and the actual
  implementation of the `configure()` function. It also defines the `get()`
  function, which can be used to get the currently used configuration object.

- [`frequenz.repo.config.nox.session`][]: Predefined nox sessions. These are
  the sessions that are used by default.

- [`frequenz.repo.config.nox.util`][]: General purpose utility functions.

### `pyproject.toml` configuration

All sessions configured by this package expect the `pyproject.toml` file to
define specific *dev* dependencies that will be used by the different `nox`
sessions.

The following optional dependencies are used and must be defined:

- `dev-docstrings`: Dependencies to lint the documentation.

  At least these packages should be included:

  - `pydocstyle`: To check the docstrings' format.
  - `darglint`: To check the docstrings' content.

- `dev-formatting`: Dependencies to check the code's formatting.

  At least these packages should be included:

  - `black`: To check the code's formatting.
  - `isort`: To check the imports' formatting.

- `dev-mypy`: Dependencies to run `mypy` to check the code's type annotations.

  At least these packages should be included:

  - `mypy`: To check the code's type annotations.

- `dev-pylint`: Dependencies to run `pylint` to lint the code.

  At least these packages should be included:

  - `pylint`: To lint the code.

- `dev-pytest`: Dependencies to run the tests using `pytest`.

  At least these packages should be included:

  - `pytest`: To run the tests.

For some of these you should install too any other dependencies that are used
by the project. For example, if the project uses `pytest-asyncio`, you should
include it in the `dev-pytest` optional dependency.

It is also recommended, but not required, to provide a global `dev` optional
dependency that includes all the other optional dependencies, so users can
install all the dependencies needed while developing the project without having
to run `nox`, which might be a bit slow if you want to do quick iterations.

```console
$ pip install -e .[dev]
...
$ pytest
...
```

Here is a sample `pyproject.toml` file that defines all the optional
dependencies:

```toml
[project]
name = "my-package"
# ...

[project.optional-dependencies]
dev-docstrings = ["pydocstyle == 6.3.0", "darglint == 1.8.1"]
dev-formatting = ["black == 23.3.0", "isort == 5.12.0"]
dev-mypy = [
  "mypy == 1.1.1",
  # For checking tests
  "my-package[dev-pytest]",
]
dev-pylint = [
  "pylint == 2.17.1",
  "pylint-google-style-guide-imports-enforcing == 1.3.0",
  # For checking tests
  "my-package[dev-pytest]",
]
dev-pytest = [
  "pytest == 7.2.2",
  "pytest-asyncio == 0.21.0",
  "pytest-mock == 3.10.0",
]
dev = [
  "my-package[dev-docstrings,dev-formatting,dev-mypy,dev-nox,dev-pylint,dev-pytest]",
]
```

# APIs

## `setuptools` gRPC support

When configuring APIs it is assumed that they have a gRPC interface.

The project structure is assumed to be as follows:

- `proto/`: Directory containing the `.proto` files.
- `py/`: Directory containing the Python code. It should only provide
  a `py.typed` file and a `__init__.py` file. API repositories should not
  contain any other Python code.
- `pytests/`: Directory containing the tests for the Python code.
- `submodules/api-common-protos`: Directory containing the submodule with the
  `google/api-common-protos` repository.
- `submodules/frequenz-api-common`: Directory containing the submodule with the
  `frequenz-floss/frequenz-api-common` repository.

Normally Frequenz APIs use basic types from
[`google/api-common-protos`](https://github.com/googleapis/api-common-protos) and
[`frequenz-floss/frequenz-api-common`](https://github.com/frequenz-floss/frequenz-api-common),
so you need to make sure the proper submodules are added to your project:

```sh
mkdir submodules
git submodule add https://github.com/googleapis/api-common-protos.git \
        submodules/api-common-protos
git submodule add https://github.com/frequenz-floss/frequenz-api-common.git \
        submodules/frequenz-api-common
git commit -m "Add api-common-protos and frequenz-api-common submodules" submodules
```

Then you need to add this package as a build dependency and a few extra
dependencies to your project, for example:

```toml
requires = [
  "setuptools >= 67.3.2, < 68",
  "setuptools_scm[toml] >= 7.1.0, < 8",
  "frequenz-repo-config[api] >= 0.1.0, < 0.2.0",
]
build-backend = "setuptools.build_meta"

[project]
dependencies = [
  "frequenz-api-common >= 0.2.0, < 0.3.0",
  "googleapis-common-protos >= 1.56.2, < 2",
  "grpcio >= 1.51.1, < 2",
]
```

Note the `api` extra in `frequenz-repo-config[api]`, this will ensure all
dependencies to build the protocol files will be installed when building the
package. Of course you need to replace the version numbers with the correct
ones too.

You should also add the following configuration to your `pyproject.toml` file
to make sure the generated files are included in the wheel:

```toml
[tool.setuptools.package-dir]
"" = "py"

[tool.setuptools.package-data]
"*" = ["*.pyi"]

[tools.pytest.ini_options]
testpaths = ["pytests"]
```

Finally you need to make sure to include the generated `*.pyi` files in the
source distribution, as well as the Google api-common-protos files, as it
is not handled automatically yet
([#13](https://github.com/frequenz-floss/frequenz-repo-config-python/issues/13)).
Make sure to include these lines in the `MANIFEST.in` file:

```
recursive-include submodules/api-common-protos/google *.proto
recursive-include submodules/frequenz-api-common/proto *.proto
```

If the defaults are not suitable for you (for example you need to use more or less
submodules or your proto files are located somewhere else, you can customize how
the protocol files are generated by adding the following section to your
`pyproject.toml` file:

```toml
[tool.frequenz_repo_config.setuptools.grpc_tools]
# Location of the proto files relative to the root of the repository (default: "proto")
proto_path = "proto_files"
# Glob pattern to use to find the proto files in the proto_path (default: "*.proto")
proto_glob = "*.prt"  # Default: "*.proto"
# List of paths to pass to the protoc compiler as include paths (default:
# ["submodules/api-common-protos", "submodules/frequenz-api-common/proto"])
include_paths = ["submodules/api-common-protos"]
# Path where to generate the Python files (default: "py")
py_path = "generated"
```

Please adapt the instructions above to your project structure if you need to change the
defaults.
"""

from . import nox, setuptools
from ._core import RepositoryType

__all__ = [
    "RepositoryType",
    "nox",
    "setuptools",
]
