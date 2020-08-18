import numpy
from skimage import draw
import identification
import matplotlib.pyplot
import visualization

# load some initial precip data 
precip_data = numpy.load('precip_1996.npy', allow_pickle=True)

# set a precip threshold and narrow your region of interest
# TODO: What are out THRESHOLD units?
THRESHOLD = 0.6 
trimmed_data = numpy.where(precip_data < THRESHOLD, 0, precip_data)

# create a structural set 
struct = numpy.zeros((16, 16))
rr, cc = draw.disk((7.5, 7.5), radius=8.5)
struct[rr, cc] = 1

# identify your storms
labeled_maps = identification.identify(trimmed_data, struct)

# visualize your data
cmap = matplotlib.pyplot .get_cmap('hsv')
visualization.storms(labeled_maps, cmap, 'Identified Storms 1996', 1, show_save='save')