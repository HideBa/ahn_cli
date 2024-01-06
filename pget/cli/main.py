import click
from service import process
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
@click.argument(
    "-o",
    "--output",
    type=str,
    help="Set the name of the output file where the data will be saved.",
)
@click.argument(
    "-c",
    "--city",
    type=str,
    help="Specify the name of the city to download point cloud data for.",
)
@click.option(
    "-i",
    "--include-class",
    type=int,
    help="Include specific point cloud classes in the download. Classes should be specified in a comma-separated list.",
)
@click.option(
    "-e",
    "--exclude-class",
    type=int,
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
    type=str,
    help="Specify a file path to a clipping boundary file. The tool will use this file to clip the point cloud data to a specific area.",
)
@click.option("-p", "--preview", help="Preview the point cloud data in a 3D viewer.")
@click.option(
    "-v", "--version", help="Display the version number of the tool and exit."
)
def main(output: str, city: str, include_class, exclude_class, clip_file) -> None:
    # TODO: if include_class and exclude_class are conflicting, raise an error
    process(
        config.GEOTILES_BASE_URL,
        output,
        city,
        include_class,
        exclude_class,
        clip_file,
    )


if __name__ == "__main__":
    main()
