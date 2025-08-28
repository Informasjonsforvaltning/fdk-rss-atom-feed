"""Nox sessions."""

import sys

import nox
from nox_poetry import Session, session

locations = ["fdk_rss_atom_feed", "tests", "noxfile.py"]
nox.options.envdir = ".cache"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = (
    "lint",
    "mypy",
    "unit_tests",
    "integration_tests",
    "contract_tests",
)


@session(python=["3.12"])
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".", "pytest", "requests", "requests-mock")
    session.run(
        "pytest",
        "-m",
        "unit",
        "-rA",
        *args,
    )


@session(python=["3.12"])
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs
    session.install(".", "pytest", "pytest-docker", "requests", "requests_mock")
    session.run(
        "pytest",
        "-m",
        "integration",
        "-rA",
        *args,
    )


@session(python=["3.12"])
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".", "pytest", "pytest-docker", "requests")
    session.run(
        "pytest",
        "-m",
        "contract",
        "-rA",
        *args,
    )


@session(python=["3.12"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=["3.12"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "pep8-naming",
    )
    session.run("flake8", *args)


@session(python=["3.12"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session(python=["3.12"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["--install-types", "--non-interactive", *locations]
    session.install(
        ".", "mypy", "pytest", "nox", "nox_poetry", "flask_restful", "feedgen"
    )
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")
