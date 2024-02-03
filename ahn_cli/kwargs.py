from typing import TypedDict


class CLIArgs(TypedDict):
    output: str
    city: str
    include_class: str | None
    exclude_class: str | None
    no_clip_city: bool
    clip_file: str | None
    decimate: int | None
    radius: int | None
    preview: bool
    help: str | None
    version: str | None
