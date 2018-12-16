from bs4 import BeautifulSoup
import numpy as np
import argparse

# construct argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--svg", required = True, help = "Path to the SVG file")
ap.add_argument("-c", "--command", required = False, default = 'Nothing',
                help = "Type of the transformation applied to the SVG file")
ap.add_argument("-x", "--tx", type = float, default = 0.0,
                help = "translation in x direction")
ap.add_argument("-y", "--ty", type = float, default = 0.0,
                help = "translation in y direction")
ap.add_argument("-a", "--angle", type = float, default = 0.0,
                help = "rotation angle")
ap.add_argument("-c1", "--cx", type = float, default = 0.0,
                help = "rotation point x")
ap.add_argument("-c2", "--cy", type = float, default = 0.0,
                help = "rotation point y")
ap.add_argument("-s1", "--sx", type = float, default = 1.0,
                help = "scale of x axis")
ap.add_argument("-s2", "--sy", type = float, default = 1.0,
                help = "scale of y axis")
args = vars(ap.parse_args())

# load the SVG file we want to process and corresponding parameters
svg_file = args["svg"]
kind = args["command"]
tx = float(args["tx"])
ty = float(args["ty"])
angle = float(args["angle"])
cx = float(args["cx"])
cy = float(args["cy"])
sx = float(args["sx"])
sy = float(args["sy"])

# set output file name
output_file = "sample_output.svg"  # should be the same svg_file name later

# open the file and create BS object
svg = open(svg_file, 'r').read()
# print(svg)
soup = BeautifulSoup(svg, features = 'xml')

def decide_transformation_type(kind, tx = 0.0, ty = 0.0, angle = 0.0,
                                cx = 0.0, cy = 0.0, sx = 1.0, sy = 1.0):
    if kind == 'translate':
        transformation = "translate" + str((tx, ty))
    elif kind == 'rotate':
        transformation = "rotate" + str((angle, cx, cy))
    elif kind == 'scale':
        transformation = "scale" + str((sx, sy))
    else:
        transformation = "matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)"

    return transformation

def apply_transformation(kind, tx, ty, angle, cx, cy, sx, sy):
    # find out the attributes inside the g element
    attrs_in_g_elem = soup.find('g').attrs
    print(attrs_in_g_elem)
    # check whether there is a transform attribute in the g element
    if "transform" not in attrs_in_g_elem:
        # if there is no such attribute, create a new one
        attrs_in_g_elem["transform"] = decide_transformation_type(kind, tx, ty, angle, cx, cy, sx, sy)
    else:
        # if there is already an attribute(s), add a new one behind it
        transform = decide_transformation_type(kind, tx, ty, angle, cx, cy, sx, sy)
        attrs_in_g_elem["transform"] = attrs_in_g_elem["transform"] + " " + transform
    print(attrs_in_g_elem)

# print(soup.prettify())

apply_transformation(kind, tx, ty, angle, cx, cy, sx, sy)

with open(output_file, "w") as file:
    file.write(str(soup))
