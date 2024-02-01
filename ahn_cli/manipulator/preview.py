import laspy
import pyvista as pv


def previewer(filepath: str) -> None:
    # Read LAS file
    las = laspy.read(filepath)

    points = pv.PolyData(las.xyz)

    # Plot using PyVista
    plotter = pv.Plotter()
    plotter.add_points(points, color="blue", point_size=3)

    plotter.show()
