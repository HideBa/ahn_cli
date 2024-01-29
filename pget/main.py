from typing import Dict, Union
import click
from pyparsing import Any
from process import process
import config
from typing import Dict, Union, List
from process import process
import config


"""
Options:
 -t, --dtm                     If this is specified, DTM will be fetched; otherwise, DSM.
 -c, --city <city_name>        Specify the name of the city to download point cloud data for.
 -o, --output <file>           Set the name of the output file where the data will be saved.
 -i, --include-class <class>   Include specific point cloud classes in the download.
                               Classes should be specified in a comma-separated list.
 -e, --exclude-class <class>   Exclude specific point cloud classes from the download.
                               Classes should be specified in a comma-separated list.
 -h, --help [category]         Display help information. Optionally, specify a category to get
                               more detailed help for a specific command.
 -cf, --clip-file <file>       Specify a file path to a clipping boundary file. The tool will
                               use this file to clip the point cloud data to a specific area.
 -v, --version                 Display the version number of the tool and exit.
"""


@click.command()
# @click.option(
#     "-t",
#     "--dtm",
#     is_flag=True,
#     help="If this is specified, DTM will be fetched; otherwise, DSM.",
# )
@click.option(
    "-o",
    "--output",
    type=str,
    help="Set the name of the output file where the data will be saved.",
)
@click.option(
    "-c",
    "--city",
    type=str,
    help="Specify the name of the city to download point cloud data for.",
)
@click.option(
    "-i",
    "--include-class",
    "include_class",
    type=str,
    help="Include specific point cloud classes in the download. Classes should be specified in a comma-separated list.",
)
@click.option(
    "-e",
    "--exclude-class",
    "exclude_class",
    type=str,
    help="Exclude specific point cloud classes from the download. Classes should be specified in a comma-separated list.",
)
@click.option(
    "-h",
    "--help",
    help="Display help information. Optionally, specify a category to get more detailed help for a specific command.",
)
@click.option(
    "-cf",
    "--clip-file",
    "clip_file",
    type=str,
    help="Specify a file path to a clipping boundary file. The tool will use this file to clip the point cloud data to a specific area.",
)
@click.option("-p", "--preview", help="Preview the point cloud data in a 3D viewer.")
@click.option(
    "-v", "--version", help="Display the version number of the tool and exit."
)
@click.option("-verbose", help="Display verbose output.")
def main(**kwargs: Dict[str, Union[str, int, bool, None]]) -> None:
    output = kwargs.get("output", "")
    city = kwargs.get("city", "")
    include_classes = (
        [int(x) for x in str(kwargs.get("include_class", "")).split(",") if x]
        if kwargs.get("include_class", "")
        else None
    )
    exclude_classes = (
        [int(x) for x in str(kwargs.get("exclude_class", "")).split(",") if x]
        if kwargs.get("exclude_class", "")
        else None
    )
    clip_file = kwargs.get("clip_file")
    preview = kwargs.get("preview")

    process(
        config.GEOTILES_BASE_URL,
        output,
        city,
        include_classes,
        exclude_classes,
        clip_file,
    )


if __name__ == "__main__":
    main()
