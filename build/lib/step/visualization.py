import imageio
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
import numpy as np


def intensities(data: np.ndarray, colormap: LinearSegmentedColormap, title: str, unit: str, start_time=0,
                          show_save='both', dpi=300) -> None:
    """Produces a simple plot for data containing precipitation intensities through time. A PNG image of each time slice
    is produced as well as a GIF of all time slices. All PNG's can be shown and saved, and the GIF can only be saved.
    By default, images will be shown and saved; see show_save documentation for information on how to show or save
    images only.
    :param data: the storm data to be plotted, given as an array of dimensions Time x Rows x Cols containing
    precipitation data. To plot precipitation in a single time slice, reshape the array to dimensions (1, Rows, Cols).
    :param colormap: the colormap given to the precipitation data, given as a LinearSegmentedColormap.
    :param title: the in-image title to give each image output, given as a string.
    :param unit: the unit of the precipitation values plotted.
    :param start_time: the number of the first time slice in the data to be plotted, used in file naming and noting time
    in image outputs, where applicable, given as an integer. The default value is 0.
    :param show_save: determines whether images produced are shown, saved, or both. The default argument is 'both',
    while 'show' only shows images and 'save' only saves them.
    :param dpi: the resolution in dots per inch, given as an integer. The default value 300.
    :return: (None.)
    """
    # close all plots open for display
    plt.close('all')

    num_time_slices = data.shape[0]

    # initialize a new list to later make gif
    images = []

    for time_index in range(num_time_slices):

        # create a new figure and gridspec to arrange our plots, where the first row is much taller than the second
        fig = plt.figure(figsize=(7, 6))
        gs = GridSpec(2, 3, height_ratios=[1, 0.05], width_ratios=[0.2, 1.0, 0.2], wspace=0, hspace=0)

        # the subplot (our map) that will take up the first row of the gridspec
        ax1 = plt.subplot(gs[0, 0:3], aspect='equal')
        ax1.set_title(title)

        # fill in the plot with our data, where each color corresponds to a precipitation intensity
        plt.pcolormesh(np.ma.masked_where(data[time_index] == 0, data[time_index]), cmap=colormap,
                       vmin=np.min(data), vmax=np.max(data))

        # invert the y axis so the origin is in the upper left (not the default with pcolormesh)
        plt.gca().invert_yaxis()

        # turn off all ticks in the plot
        plt.tick_params(bottom=False, left=False, labelleft=False, labelbottom=False)
        # https://stackoverflow.com/a/12998531

        # create a colorbar
        ax2 = plt.subplot(gs[1, 1])
        cb = plt.colorbar(cax=ax2, orientation="horizontal")
        minimum = np.min(np.ma.masked_where(data == 0, data))
        maximum = np.max(data)

        # set the tick positions and their labels manually
        cb.set_ticks([0, maximum * .25, maximum * .5, maximum * .75, maximum])
        cb.set_ticklabels([round(minimum, 1), round(maximum * .25, 1), round(maximum * .5, 1), round(maximum * .75, 1),
                           round(maximum, 1)])
        cb.ax.tick_params(labelsize=7)

        # and give it a label
        cb.set_label(f'Range of precipitation intensities - {unit}', fontsize=7)

        # depending on the value of show_save, decide what to do with the image we've created
        if show_save == 'show' or show_save == 'both':
            plt.show()

        if show_save == 'save' or show_save == 'both':
            fig.savefig(f'{title} t={start_time + time_index}.png', dpi=dpi)
            images.append(imageio.imread(f'{title} t={start_time + time_index}.png'))

    # and do the same here
    if show_save == 'save' or show_save == 'both':
        imageio.mimsave(f'{title}.gif', images, fps=1.5)


def storms(data: np.ndarray, colors: LinearSegmentedColormap or list, title: str, start_time=0,
                     show_save='both', dpi=300, ticks=False) -> None:
    """Produces a simple plot for data containing labeled storms, where each label is plotted to the same color
    throughout time slices. A PNG image of each time slice is produced as well as a GIF of all time slices. All PNG's
    can be shown and saved, and the GIF can only be saved. By default, images will be shown and saved; see show_save
    documentation for information on how to show or save images only.
    :param data: the storm data to be plotted, given as an array of dimensions Time x Rows x Cols containing labeled
    storms (fully-identified, tracked, or otherwise). To plot storms in a single time slice, reshape the array to
    dimensions (1, Rows, Cols).
    :param colors: the colormap given to the storm labels. If colors is a LinearSegmentedColormap from Matplotlib,
    each label is given a unique color (when a cyclic colormap is not given), though color differentiation may suffer
    with longer runs. If colors is a Python list, labels are mapped by cycling through the list as a ListedColormap,
    which can lead to unfortunate color collisions.
    :param title: the in-image title to give each image output, given as a string.
    :param start_time: the number of the first time slice in the data to be plotted, used in file naming and noting time
    in image outputs, where applicable, given as an integer. The default value is 0.
    :param: show_save: determines whether images produced are shown, saved, or both. The default argument is 'both',
    while 'show' only shows images and 'save' only saves them.
    :param dpi: the resolution in dots per inch, given as an integer. The default value is 300.
    :param ticks: the toggle for including ticks in the plot, given as a boolean. The default value is False and turning
    on ticks stops the current time slice from being displayed to avoid overlap.
    :return: (None.)
    """
    # close all plots open for display
    plt.close('all')

    num_time_slices = data.shape[0]

    # initialize a new list to later make gif
    images = []

    # if the colormap we are given is a list, extend it to cycle through the number of storms we'll need to color in
    # the data and create a ListedColormap object from this list
    if isinstance(colors, list):
        num_storms = len(np.unique(data)) - 1
        num_colors = len(colors)

        extend_colors = []
        while len(extend_colors) < num_storms:
            diff = num_storms - len(extend_colors)
            if diff >= num_colors:
                extend_colors.extend(colors)
            else:
                extend_colors.extend(colors[:diff])

        colormap = ListedColormap(extend_colors)
    else:
        colormap = colors

    for time_index in range(num_time_slices):

        # as above, create a new figure and gridspec to arrange our plots, where the first row is much taller than the
        # second
        fig = plt.figure(figsize=(7, 6))
        gs = GridSpec(2, 3, height_ratios=[1, 0.05], width_ratios=[0.2, 1.0, 0.2], wspace=0, hspace=0)

        # the subplot (our map) that will take up the first row of the gridspec
        ax1 = plt.subplot(gs[0, 0:3], aspect='equal')
        ax1.set_title(title)

        # set the 'color levels' to display correctly depending on the type of colormap
        if isinstance(colormap, LinearSegmentedColormap):
            levels = list(np.arange(0, np.max(data) + 1))
        else:
            levels = list(np.arange(1, np.max(data) + 1))

        # generate a colormap index based on discrete intervals (from Matplotlib)
        norm = BoundaryNorm(levels, ncolors=colormap.N, clip=True)

        # fill in the plot with our data, where each color corresponds to either a unique storm label (if we have a
        # LinearSegmentedColormap) or cycles through a list of colors (if we have a ListedColormap)
        plt.pcolormesh(np.ma.masked_where(data[time_index] == 0, data[time_index]), cmap=colormap, norm=norm)
        # https://stackoverflow.com/a/51384954

        # invert the y axis so the origin is in the upper left (not the default with pcolormesh)
        plt.gca().invert_yaxis()

        # if ticks are toggled off, turn them off
        if ticks == False:
            plt.tick_params(bottom=False,  left=False, labelleft=False, labelbottom=False)
            # https://stackoverflow.com/a/12998531

            # add the time index corresponding to the data in the image
            fig.suptitle(f't = {start_time + time_index}', fontsize=10, y=0.045)

        # depending on the value of show_save, decide what to do with the image we've created
        if show_save == 'show' or show_save == 'both':
            plt.show()

        if show_save == 'save' or show_save == 'both':
            fig.savefig(f'{title} t={start_time + time_index}.png', dpi=dpi)
            images.append(imageio.imread(f'{title} t={start_time + time_index}.png'))

    # and do the same here
    if show_save == 'save' or show_save == 'both':
        imageio.mimsave(f'{title}.gif', images, fps=1.5)


def histogram(data: np.ndarray, bins: int, bin_range: tuple, title='Frequency of Precipitation Intensities',
              show_save='both') -> None:
    """Produces a histogram depicting the frequency of precipitation values over a set of time slices to aid in finding
    an optimal precipitation threshold.
    :param data: the data from which to construct the histogram.
    :param bins: the number of equal-width bins in the range; see
    matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.hist.html.
    :param bin_range: the lower and upper range of the bins; see above.
    :param: title: the title both of the histogram and the PNG file. The default title is
    'Frequency of Precipitation Intensities'.
    :param: show_save: determines whether images produced are shown, saved, or both. The default argument is 'both',
    while 'show' only shows images and 'save' only saves them.
    :return: (None - the resulting histogram is shown and saved.)
    """
    # reshape our data into a 2d array to more easily make sure all data is included in the histogram
    if data.ndim == 3:
        hist_data = data.reshape((data.shape[0] * data.shape[1]), data.shape[2])
        # https://stackoverflow.com/a/51159213
    else:
        hist_data = data

    # call Matplotlib's hist with the specified parameters for bins and range
    plt.hist(hist_data, bins=bins, range=bin_range)
    plt.title(title)
    plt.xlabel('Precipitation intensities')
    plt.ylabel('Number of Occurrences')
    if show_save == 'both' or show_save == 'save':
        plt.savefig(f'{title}.png')
    if show_save == 'both' or show_save == 'show':
        plt.show()
