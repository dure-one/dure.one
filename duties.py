"""Development tasks."""

from __future__ import annotations

import os
import re
import sys
from contextlib import contextmanager
from functools import wraps
from importlib.metadata import version as pkgversion
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from duty import duty, tools

if TYPE_CHECKING:
    from collections.abc import Iterator

    from duty.context import Context


PY_SRC_PATHS = (Path(_) for _ in ("src", "duties.py"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)
CI = os.environ.get("CI", "0") in {"1", "true", "yes", ""}
WINDOWS = os.name == "nt"
PTY = not WINDOWS and not CI
MULTIRUN = os.environ.get("MULTIRUN", "0") == "1"


def pyprefix(title: str) -> str:
    if MULTIRUN:
        prefix = f"(python{sys.version_info.major}.{sys.version_info.minor})"
        return f"{prefix:14}{title}"
    return title


def not_from_insiders(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(ctx: Context, *args: Any, **kwargs: Any) -> None:
        origin = ctx.run("git config --get remote.origin.url", silent=True)
        if "pawamoy-insiders/griffe" in origin:
            ctx.run(
                lambda: False,
                title="Not running this task from insiders repository (do that from public repo instead!)",
            )
            return
        func(ctx, *args, **kwargs)

    return wrapper


@contextmanager
def material_insiders() -> Iterator[bool]:
    if "+insiders" in pkgversion("mkdocs-material"):
        os.environ["MATERIAL_INSIDERS"] = "true"
        try:
            yield True
        finally:
            os.environ.pop("MATERIAL_INSIDERS")
    else:
        yield False


def _get_changelog_version() -> str:
    changelog_version_re = re.compile(r"^## \[(\d+\.\d+\.\d+)\].*$")
    with Path(__file__).parent.joinpath("CHANGELOG.md").open("r", encoding="utf8") as file:
        return next(filter(bool, map(changelog_version_re.match, file))).group(1)  # type: ignore[union-attr]


@duty
def changelog(ctx: Context, bump: str = "") -> None:
    """Update the changelog in-place with latest commits.

    Parameters:
        bump: Bump option passed to git-changelog.
    """
    if (bump != None):
        ctx.run(tools.git_changelog(bump=bump or None), title="Updating changelog")
    else:
        ctx.run(tools.git_changelog(repository=".",
    output="CHANGELOG.md",
    convention="angular",
    provider="github",
    template="keepachangelog",
    parse_trailers=True,
    parse_refs=False,
    sections=("build", "deps", "feat", "fix", "refactor"),
    versioning="pep440",
    bump="auto",
    in_place=True), title="Updating changelog")
    # ctx.run(tools.yore.check(bump=bump or _get_changelog_version()), title="Checking legacy code")


@duty(pre=["check-quality", "check-docs"])
def check(ctx: Context) -> None:
    """Check it all!"""


@duty
def check_quality(ctx: Context) -> None:
    """Check the code quality."""
    ctx.run(
        tools.ruff.check(*PY_SRC_LIST, config="config/ruff.toml"),
        title=pyprefix("Checking code quality"),
    )


@duty
def check_docs(ctx: Context) -> None:
    """Check if the documentation builds correctly."""
    Path("htmlcov").mkdir(parents=True, exist_ok=True)
    Path("htmlcov/index.html").touch(exist_ok=True)
    with material_insiders():
        ctx.run(
            tools.mkdocs.build(strict=True, verbose=True),
            title=pyprefix("Building documentation"),
        )


@duty
def docs(ctx: Context, *cli_args: str, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the documentation (localhost:8000).

    Parameters:
        host: The host to serve the docs from.
        port: The port to serve the docs on.
    """
    with material_insiders():
        ctx.run(
            tools.mkdocs.serve(dev_addr=f"{host}:{port}").add_args(*cli_args),
            title="Serving documentation",
            capture=False,
        )
