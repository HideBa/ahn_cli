import laspy
import polyscope as ps


def previewer(filepath: str) -> None:
    # Read LAS file
    las = laspy.read(filepath)
    points = las.xyz

    ps.init()
    _ps_cloud = ps.register_point_cloud("AHN Point Cloud", points)

    ps.show()
