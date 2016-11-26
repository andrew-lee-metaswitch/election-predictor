import shapefile
from shapely.geometry import box, shape

# Use 8 sf decimals throughout
from decimal import Decimal, getcontext

getcontext().prec = 8

SHAPEFILE_FOLDER = 'data/shapes/'
REFERENDUM_DISTRICT_SHAPES = 'unitary_electoral_division_region'
WESTMINSTER_DISTRICT_SHAPES = 'westminster_const_region'

# Load the shapefiles here to only load them once
DISTS = shapefile.Reader(SHAPEFILE_FOLDER + REFERENDUM_DISTRICT_SHAPES)
CONSTS = shapefile.Reader(SHAPEFILE_FOLDER + WESTMINSTER_DISTRICT_SHAPES)

CONST_IDS = [record[8] for record in CONSTS.records()]


def overlaps(shapea, shapeb):
    """ Overlaping is where there is a non-trivial intersection """
    return shapea.intersects(shapeb) and not shapea.touches(shapeb)


def get_area_overlap(const_id):
    """
        Return a dictionary containing the percentage of the constituency
        that is in each intersecting electoral area
    """
    assert const_id in CONST_IDS, \
        "Unknown constituency: {0}".format(const_id)

    intersection_dict = {}
    const_shape = CONSTS.shapes()[CONST_IDS.index(const_id)]
    const_bbox = box(*const_shape.bbox)
    const_poly = shape(const_shape.__geo_interface__)

    for elec_dist in DISTS.shapeRecords():
        if overlaps(box(*elec_dist.shape.bbox), const_bbox):
            elec_poly = shape(elec_dist.shape.__geo_interface__)
            if const_poly.contains(elec_poly):
                intersection_dict[elec_dist.record[0]] = 1.0
            elif overlaps(elec_poly, const_poly):
                isection = elec_poly.intersection(const_poly)
                intersection_dict[elec_dist.record[0]] = \
                    Decimal(isection.area) / Decimal(elec_poly.area)
                if elec_poly.contains(const_poly):
                    break

    return intersection_dict
