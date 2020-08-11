import imageio
from matplotlib.colors import BoundaryNorm
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


def storms_with_map(data, title, lat, long, start_time):
    """Example function for how to plot tracking results over a map. May not generalize based on data and custom Basemap
    would need to be specified.
    :param data: the storm data to be plotted, given as an array of dimensions Time x Rows x Cols containing labeled
    tracked storms. To plot storms in a single time slice, reshape the array to dimensions (1, Rows, Cols).
    :param title: the in-image title to give each image output, given as a string.
    :param lat: the latitude data corresponding to each [row][col] in tracked_storms, given as an array of dimensions
    1 x Rows x Cols.
    :param long: the longitude data corresponding to each [row][col] in tracked_storms, given as an array of dimensions
    1 x Rows x Cols.
    :param start_time: the number of the first time slice in the data to be plotted, used in file naming and noting time
    in image outputs, where applicable, given as an int.
    :return: (None.)
    """
    # close all plots open for display
    plt.close('all')

    num_time_slices = data.shape[0]

    # reshape our lat and long data to 2d arrays
    long = long.reshape(long.shape[1], long.shape[2])
    lat = lat.reshape(lat.shape[1], lat.shape[2])

    # initialize a new list to later make gif
    images = []

    for time_index in range(num_time_slices):

        # create a new figure and gridspec to arrange our plots, where the first row is much taller than the second
        fig = plt.figure(figsize=(7, 6))
        gs = GridSpec(2, 3, height_ratios=[1, 0.05], width_ratios=[0.2, 1.0, 0.2], wspace=0, hspace=0)

        # the subplot (our map) that will take up the first row of the gridspec
        ax1 = plt.subplot(gs[0, 0:3])
        ax1.set_title(title)

        # create a Basemap that captures the lats and longs corresponding to our data well
        m = Basemap(width=7550000, height=6550000, projection='lcc', resolution='c', lat_1=45., lat_2=55, lat_0=52.5, lon_0=-106.)

        # give continents a color and transparency
        m.fillcontinents(color='#bdbdbd', alpha=0.3)

        # link our lat and long data to the map
        x, y = m(long, lat)

        # set the 'color levels' to display correctly
        levels = list(np.arange(0, np.max(data) + 1))

        # use the hsv colormap
        cmap = plt.get_cmap('hsv')

        # generate a colormap index based on discrete intervals (from Matplotlib)
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

        # fill in the grid on the map with our data and color-code it by levels defined above
        m.pcolormesh(x=x, y=y, data=np.ma.masked_where(data[time_index] == 0, data[time_index]), cmap=cmap, norm=norm)

        # create a colorbar
        ax2 = plt.subplot(gs[1, 1])
        CB = plt.colorbar(cax=ax2, orientation="horizontal")

        # set the tick positions and their labels manually
        positions = list(np.unique(data[time_index]) - 0.5)
        positions.remove(-0.5)
        CB.set_ticks(positions)
        labels = list(np.unique(data[time_index]))
        labels.remove(0)
        CB.set_ticklabels(labels)
        CB.ax.tick_params(labelsize=7)

        # label the colorbar
        CB.set_label(f'Labels of active storms in t={start_time + time_index}', fontsize=7)

        plt.show()

        # show and save image
        fig.savefig(f'map plot t={start_time + time_index}.png', dpi=300)
        images.append(imageio.imread(f'map plot t={start_time + time_index}.png'))

    # construct a gif from the images we've saved
    imageio.mimsave(f'map_plot.gif', images, fps=1.5)
