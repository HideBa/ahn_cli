import laspy
import pyvista as pv


def main() -> None:
    # Read LAS file
    las = laspy.read("./pget/core/point_cloud/tiny_thinned.las")

    points = pv.PolyData(las.xyz)

    # Plot using PyVista
    plotter = pv.Plotter()
    plotter.add_points(points, color="blue", point_size=3)

    plotter.show()


if __name__ == "__main__":
    main()
