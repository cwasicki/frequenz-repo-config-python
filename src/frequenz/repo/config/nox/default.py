# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Default nox configuration for different types of repositories.

This module provides the default configuration for the different types of
repositories defined by
[`frequenz.repo.config.RepositoryType`][frequenz.repo.config.RepositoryType].

The `actor_config`, `api_config`, `app_config`, `lib_config`, and `model_config`
variables are the default configurations for libraries, APIs, actors and applications,
respectively. The `common_config` variable is the default configuration for all types of
repositories.

The `actor_command_options`, `api_command_options`, `app_command_options`,
`lib_command_options`, and `model_command_options` variables are the default
command-line options for the same types of repositories, and the
`common_command_options` variable is the default command-line options for all types of
repositories.

They can be modified before being passed to
[`nox.configure()`][frequenz.repo.config.nox.configure] by using the
[`CommandsOptions.copy()`][frequenz.repo.config.nox.config.CommandsOptions.copy]
method.
"""

import dataclasses

from . import config as _config
from . import util as _util

common_command_options: _config.CommandsOptions = _config.CommandsOptions(
    black=[
        "--check",
    ],
    darglint=[
        "-v2",  # for verbose error messages.
    ],
    isort=[
        "--check",
    ],
    mypy=[
        "--install-types",
        "--namespace-packages",
        "--non-interactive",
        "--explicit-package-bases",
        "--strict",
    ],
    # SDK: pylint "--extension-pkg-whitelist=pydantic"
    pytest=[
        "-W=all",
        "-vv",
    ],
)
"""Default command-line options for all types of repositories."""

common_config = _config.Config(
    opts=common_command_options.copy(),
    sessions=[
        "formatting",
        "mypy",
        "pylint",
        "docstrings",
        "pytest_min",
        "pytest_max",
    ],
    source_paths=[
        "src",
    ],
    extra_paths=[
        "benchmarks",
        "docs",
        "examples",
        "noxfile.py",
        "tests",
    ],
)
"""Default configuration for all types of repositories."""

actor_command_options: _config.CommandsOptions = common_command_options.copy()
"""Default command-line options for actors."""

actor_config: _config.Config = common_config.copy()
"""Default configuration for actors."""

api_command_options: _config.CommandsOptions = common_command_options.copy()
"""Default command-line options for APIs."""

api_config: _config.Config = dataclasses.replace(
    common_config,
    opts=api_command_options,
    # We don't check the sources at all because they are automatically generated.
    source_paths=[],
    # We adapt the path to the tests.
    extra_paths=list(_util.replace(common_config.extra_paths, {"tests": "pytests"})),
)
"""Default configuration for APIs.

Same as `common_config`, but with `source_paths` replacing `"src"` with `"py"`
and `extra_paths` replacing `"tests"` with `"pytests"`.
"""

app_command_options: _config.CommandsOptions = common_command_options.copy()
"""Default command-line options for applications."""

app_config: _config.Config = common_config.copy()
"""Default configuration for applications."""

lib_command_options: _config.CommandsOptions = common_command_options.copy()
"""Default command-line options for libraries."""

lib_config: _config.Config = common_config.copy()
"""Default configuration for libraries."""

model_command_options: _config.CommandsOptions = common_command_options.copy()
"""Default command-line options for models."""

model_config: _config.Config = common_config.copy()
"""Default configuration for models."""
