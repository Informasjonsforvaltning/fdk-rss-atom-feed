"""Nox sessions."""
import sys

import nox
from nox_poetry import Session, session

locations = ["fdk_rss_atom_feed", "tests", "main.py", "noxfile.py"]
nox.options.envdir = ".cache"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = (
    "lint",
    "mypy",
    "safety",
    "unit_tests",
    "integration_tests",
    "contract_tests",
)


@session
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".", "pytest")
    session.run(
        "pytest",
        "-m",
        "unit",
        "-rA",
        *args,
    )


@session
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs
    session.install(".", "pytest", "pytest-docker")
    session.run(
        "pytest",
        "-m",
        "integration",
        "-rA",
        *args,
    )


@session
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".", "pytest")
    session.run(
        "pytest",
        "-m",
        "contract",
        "-rA",
        *args,
    )


@session
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session
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


@session
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["--install-types", "--non-interactive", *locations]
    session.install(
        ".", "mypy", "pytest", "nox", "nox_poetry", "flask_restful", "feedgen"
    )
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", f"--file={requirements}", "--bare")
