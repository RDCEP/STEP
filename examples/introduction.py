import copy
import identification as idf
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
import visualization as viz
from examples import plot_with_map as map_plot
import quantification as qu
from skimage import draw
import tracking as tr


"""
Here we give some package use examples to help get the user get started. Please see the README and function docstrings 
for details about function usage.
"""

# first, let's set a precipitation threshold constant
THRESHOLD = 0.6   # WAS 0.075 FOR NICE 1995 ID RUN

# # and open some precipitation data
# file = 'data/1996_CCSMBC_3hr_rain_tend.nc'
# data = nc.Dataset(file)
#
# # select a temporal subset of the data
# rain_exp_data = data['rain_exp'][1:6]
# rain_con_data = data['rain_con'][1:6]
#
# # if we are given both large scale and convective precipitation data, add these element-wise
# test_data = rain_exp_data + rain_con_data
#
# # if we are given data with a mask, fill masked values with 0
# filled_data = test_data.filled(0)

# FOR BEN:
filled_data = np.load('data/precip_1996.npy', allow_pickle=True)

# generate binary data to work with if we wish (though this is not necessary)
binary_data = np.where(filled_data < THRESHOLD, 0, 1)

# and generate filled precipitation data
# this may also be used for the identification algorithm
precip_data = np.where(filled_data < THRESHOLD, 0, filled_data)

# if we want, we can see and save a plot of the precipitation intensities using show_save_
# first, we need to give decide on a colormap for our intensity plot
cmap = plt.get_cmap('gnuplot').reversed()

# let's specify a title, unit, start time, and only show the image
viz.show_save_intensities(precip_data, cmap, 'Precipitation Intensities 1996',
                           'mm (3h\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE})', start_time=1, show_save='show')

# now, to identify storms we first need to construct a custom structural set (most likely a disk)
struct = np.zeros((16, 16))
rr, cc = draw.disk((7.5, 7.5), radius=8.5)
struct[rr, cc] = 1
# https://stackoverflow.com/a/41495033

# if we need to find an appropriate precipitation threshold, we can create a histogram from the data to aid in finding a
# precipitation threshold
viz.histogram(filled_data, 3, (0, 2))

# the algorithms take 3d (Time x Rows x Cols) arrays, so if we have a 2d array, we need to reshape it to include a phony
# third dimension
if binary_data.ndim == 2:
    binary_data = binary_data.reshape(1, binary_data.shape[0], binary_data.shape[1])

# to compute the identification algorithm, we simply supply the data and our morphological structure
labeled_maps = idf.identify(binary_data, struct)

# to see the results of our work, we can use show_save_storms, but first let's try a different colormap
cmap = plt.get_cmap('hsv')
viz.show_save_storms(labeled_maps, cmap, 'Identified Storms 1996', 1, show_save='show')

# to save the result, we can use np save
np.save('labeled_maps.npy', labeled_maps)

# and to load it, we can use np load
# labeled_maps = np.load('labeled_maps.npy', allow_pickle=True)

# we might want to keep a copy of labeled_maps if we haven't saved it before tracking storms since it will be passed by
# reference
id_result = copy.deepcopy(labeled_maps)

# and we can now track storms by supplying the necessary data and user-specified values - see the README and docstring
# information for more on this
# if we're still figuring out the optimal values for our data, we can turn 'test' on, which prints information about the
# decisions the algorithm is making, which can then help us tune our parameters
# NOTE: the result of this calculation is provided below, so the user does not have to wait if they wish
# tracked_storms = tr.track(labeled_maps, precip_data, 0.7, 0.003, 18.6, test=True)

# and once again we can save this if we're happy with the result - this is probably a good idea since storm tracking is
# very computationally expensive
# np.save('tracked_storms_1996.npy', tracked_storms)

# let's load the result of the calculation above to save time
tracked_storms = np.load('data/tracked_storms_1996.npy', allow_pickle=True)

# now we can use show_save_storms again for a sample plot of our results
viz.show_save_storms(tracked_storms, cmap, 'Tracked Storms 1996', 1, show_save='show')

# if latitudes and longitudes haven't been provided as variables in the original nc file, we can read those in similarly
file = 'data/lat_long_1996.nc'
data = nc.Dataset(file)
lat_data = data['XLAT'][:]
long_data = data['XLONG'][:]

# if we wish to plot over a map, we can do so in a similar fashion to the example function given by the following
# NOTE: this precipitation data and corresponding lat/long data are provided south to north, so when plotted on a map
# with this orientation, the y axis must be inverted
map_plot.storms_with_map(tracked_storms, 'Tracked Storms with Map 1996', lat_data, long_data, 1)

# now we can also compute characteristics of these storms by supplying some additional information about the data
# since the central location also depends on lat/long data, we must interpret these results with the orientation of our
# plot over a map in mind
storm_chars = qu.quantify(tracked_storms, precip_data, lat_data, long_data, 3, 16)
