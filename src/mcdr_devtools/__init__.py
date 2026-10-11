"""Development tools for MCDReforged.

The names defined here are scaffolding for the documentation build, so
autodoc has something to render. Replace them as real tools land.
"""

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcdr-devtools")
except PackageNotFoundError:
    # Source tree that has not been installed as a package.
    __version__ = "unknown"

__all__ = ["__version__", "DevToolsError", "ToolName", "ToolSpec", "describe"]

type ToolName = str
"""Name that identifies a tool."""


class DevToolsError(Exception):
    """Raised when a tool spec cannot be used."""


@dataclass(frozen=True)
class ToolSpec:
    """Description of a single tool.

    :param name: unique name of the tool.
    :param summary: one-line description of what the tool does, empty when
        the tool has no summary to show.
    """

    name: ToolName
    summary: str = ""


def describe(spec: ToolSpec) -> str:
    """Renders ``spec`` as one display line.

    :param spec: the tool to describe.
    :returns: ``"<name>: <summary>"``, or the bare name when the summary is
        empty.
    """
    return f"{spec.name}: {spec.summary}" if spec.summary else spec.name
