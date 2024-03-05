# AHN CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version: 1.0.0](https://img.shields.io/badge/Version-0.1.8-green.svg)](https://github.com/HideBa/ahn-cli/releases/tag/v0.1.8)
[![CICD Status: Passing](https://img.shields.io/badge/CICD-Passing-brightgreen.svg)](https://github.com/HideBa/ahn-cli/actions)

## Description

AHN CLI is a command-line interface tool designed for the effortless downloading of AHN (Actueel Hoogtebestand Nederland) point cloud data for specific cities and classification classes.

## Installation

Install AHN CLI using pip:

```
pip install ahn_cli
```

## Usage

To utilize the AHN CLI, execute the following command with the appropriate options:

```shell
Options:
 -c, --city <city_name>        Download point cloud data for the specified city.
 -o, --output <file>           Designate the output file for the downloaded data.
 -i, --include-class <class>   Include specific point cloud classes in the download,
                               specified in a comma-separated list. Available classes:
                               0:Created, never classified; 1:Unclassified; 2:Ground;
                               6:Building; 9:Water; 14:High tension; 26:Civil structure.
 -e, --exclude-class <class>   Exclude specific point cloud classes from the download,
                               specified in a comma-separated list. Available classes as above.
 -d, --decimate <step>         Decimate the point cloud data by the specified step.
 -ncc, --no-clip-city          Avoid clipping the point cloud data to the city boundary.
 -cf, --clip-file <file>       Provide a file path for a clipping boundary file to clip
                               the point cloud data to a specified area.
 -e, --epsg <epsg>             Set the EPSG code for user's clip file.
 -b, --bbox <bbox>             Specify a bounding box to clip the point cloud data. It should be comma-separated list with minx,miny,maxx,maxy
                               centered on the city polygon.
 -p, --preview                 Preview the point cloud data in a 3D viewer.
 -h, --help [category]         Show help information. Optionally specify a category for
                               detailed help on a specific command.
 -v, --version                 Display the version number of the AHN CLI and exit.
```

### Usage Examples

**Download Point Cloud Data for Delft with All Classification Classes:**

```
ahn_cli -c delft -o ./delft.laz
```

**To Include or Exclude Specific Classes:**

```
ahn_cli -c delft -o ./delft.laz -i 1,2
```

**For Non-Clipped, Rectangular-Shaped Data:**

```
ahn_cli -c delft -o ./delft.laz -i 1,2 -ncc
```

**To Decimate City-Scale Point Cloud Data:**

```
ahn_cli -c delft -o ./delft.laz -i 1,2 -d 2
```

**Specify a Bounding box for clipping:**

If you specify a `b`, it will clip the point cloud data with specified bounding box.
```
ahn_cli -c delft -o ./delft.laz -i 1,2 -d 2 -b 194198.302994,443461.343994,194594.109009,443694.838989
```


## Reporting Issues

Encountering issues or bugs? We greatly appreciate your feedback. Please report any problems by opening an issue on our GitHub repository. Be as detailed as possible in your report, including steps to reproduce the issue, the expected outcome, and the actual result. This information will help us address and resolve the issue more efficiently.

## Contributing

Your contributions are welcome! If you're looking to contribute to the AHN CLI project, please first review our Contribution Guidelines. Whether it's fixing bugs, adding new features, or improving documentation, we value your help.

To get started:

- Fork the repository on GitHub.
- Clone your forked repository to your local machine.
- Create a new branch for your contribution.
- Make your changes and commit them with clear, descriptive messages.
  Push your changes to your fork.
- Submit a pull request to our repository, providing details about your changes and the value they add to the project.
- We look forward to reviewing your contributions and potentially merging them into the project!
