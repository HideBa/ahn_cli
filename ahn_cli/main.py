from typing import cast
import click
from pyparsing import Any
from ahn_cli.kwargs import CLIArgs
from ahn_cli.validator import validate_all
from ahn_cli.process import process
from ahn_cli import config


"""
Options:
 -c, --city <city_name>        Specify the name of the city to download point cloud data for.
 -o, --output <file>           Set the name of the output file where the data will be saved.
 -i, --include-class <class>   Include specific point cloud classes in the download.
                               Classes should be specified in a comma-separated list.
 -e, --exclude-class <class>   Exclude specific point cloud classes from the download.
                               Classes should be specified in a comma-separated list.
 -d, --decimate <step>         Decimate the point cloud by a given step.
 -ncc --no-clip-city           Do not clip the point cloud data to the city boundary.
 -cf, --clip-file <file>       Specify a file path to a clipping boundary file. The tool will
                               use this file to clip the point cloud data to a specific area.
 -r, --radius <radius>         Set the radius of the circle to clip the point cloud data to. Unit is in meter.
 -p, --preview                 Preview the point cloud data in a 3D viewer.
 -h, --help [category]         Display help information. Optionally, specify a category to get
                               more detailed help for a specific command.
 -v, --version                 Display the version number of the tool and exit.
"""


@click.command()
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
    help="Include specific point cloud classes in the download. Classes should be specified in a comma-separated list. Here is a list of available classes. 0:Created,never classifed 1:Unclassified 2:Ground 6:Building 9:Water 14:High tension 26:Civil structure",
)
@click.option(
    "-e",
    "--exclude-class",
    "exclude_class",
    type=str,
    help="Exclude specific point cloud classes from the download. Classes should be specified in a comma-separated list.Here is a list of available classes. 0:Created,never classifed 1:Unclassified 2:Ground 6:Building 9:Water 14:High tension 26:Civil structure",
)
@click.option(
    "-ncc",
    "--no-clip-city",
    is_flag=True,
    help="Do not clip the point cloud data to the city boundary.",
)
@click.option(
    "-cf",
    "--clip-file",
    "clip_file",
    type=str,
    help="Specify a file path to a clipping boundary file. The tool will use this file to clip the point cloud data to a specific area.",
)
@click.option(
    "-d",
    "--decimate",
    type=int,
    help="Decimate the point cloud by a given step.",
)
@click.option(
    "-r",
    "--radius",
    type=int,
    help="Set the radius of the circle to clip the point cloud data to. Unit is in meter.",
)
@click.option(
    "-p",
    "--preview",
    is_flag=True,
    help="Preview the point cloud data in a 3D viewer.",
)
@click.option(
    "-h",
    "--help",
    help="Display help information. Optionally, specify a category to get more detailed help for a specific command.",
    multiple=True,  # Allow multiple lines for help information.
)
@click.option(
    "-v", "--version", help="Display the version number of the tool and exit."
)
@click.option("-verbose", help="Display verbose output.")
def main(**kwargs: Any) -> None:
    cfg = config.Config()
    params = cast(CLIArgs, kwargs)
    output = params.get("output", "")
    city = params.get("city", "")
    include_classes = (
        [int(x) for x in str(params.get("include_class", "")).split(",") if x]
        if params.get("include_class", "")
        else None
    )
    exclude_classes = (
        [int(x) for x in str(params.get("exclude_class", "")).split(",") if x]
        if params.get("exclude_class", "")
        else None
    )
    no_clip_city = params.get("no_clip_city")
    clip_file = params.get("clip_file")
    decimate = params.get("decimate")
    radius = params.get("radius")
    preview = params.get("preview")
    if validate_all(
        cfg,
        output,
        city,
        include_classes,
        exclude_classes,
        no_clip_city,
        clip_file,
        decimate,
        radius,
    ):
        process(
            cfg.geotiles_base_url,
            cfg.city_polygon_file,
            output,
            city,
            include_classes,
            exclude_classes,
            no_clip_city,
            clip_file,
            radius,
            preview,
        )


if __name__ == "__main__":
    main()
