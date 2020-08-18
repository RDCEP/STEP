# STEP (Storm Tracking and Evaluation Protocol)

STEP is a Python package that identifies, tracks, and computes physical characteristics of rainstorms given spatiotemporal precipitation data. The algorithms herein are implementations of those proposed by Chang et al. in [*Changes in Spatiotemporal Precipitation Patterns in Changing Climate Conditions*](https://geosci.uchicago.edu/~moyer/MoyerWebsite/Publications/Papers/Changes_Spatio-temporal_Precipitation_patterns.pdf), released by the [Center for Robust Decision-making on Climate and Energy Policy](https://www.rdcep.org). For implementation details, see the [wiki](https://github.com/bkleeman/STEP-suggestions/wiki).

*Note: Due to the time and space complexity of the computations used to track storms, you may struggle to run the tracking algorithm on a general purpose computer. We suggest using specialized hardware for tracking.*

## Installation

`git clone https://github.com/relttira/STEP.git`  
`$ python setup.py install`


<!--- To install STEP, use the package manager [pip](https://pip.pypa.io/en/stable/). --->

## Dependencies
|Name|Version|
|--|--|
|[imageio](https://imageio.readthedocs.io/en/stable/installation.html)|2.8.0|
|[Matplotlib](https://matplotlib.org/3.2.2/users/installing.html)|3.2.1|
|[netCDF4](https://unidata.github.io/netcdf4-python/netCDF4/index.html)|1.5.3|
|[NumPy](https://numpy.org/install/)|1.18.5|
|[scikit-image](https://scikit-image.org/docs/dev/install.html)|0.17.2|
|[SciPy](https://www.scipy.org/install.html)|1.4.1|

 *[Basemap](https://matplotlib.org/basemap/users/installing.html) is necessary when using the example plotting function `storms_with_map` found in the [Tutorial](https://github.com/relttira/STEP/wiki/Tutorial). Additionally, the results of the package can be plotted using your visualization library of choice.*
## Usage
`cd step` and create a `test.py` file
```
# load some initial precip data 
precip_data = numpy.load('precip_1996.npy', allow_pickle=True)

# set a precip threshold and narrow your region of interest
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
```

Run the file and see the output:

![Results in GIF format](https://media.giphy.com/media/fuKHtjrF4btvIjxMKp/giphy.gif)

Please see the [Tutorial](https://github.com/relttira/STEP/wiki/Tutorial) for a comprehensive introduction.  
The [Implementation Details wiki](https://github.com/relttira/wiki/Implementation-Details) provides function signatures and usage tips.  
-- You can also call [`help`](https://docs.python.org/3/library/functions.html#help)`(function)` in your python script for more info. Command line interface yet to come.

Both the [Methodology wiki](https://github.com/relttira/STEP/wiki/Methodology) and the [original publication](https://geosci.uchicago.edu/~moyer/MoyerWebsite/Publications/Papers/Changes_Spatio-temporal_Precipitation_patterns.pdf) include background information on the reasoning behind the algorithms.

## Contributing
Feel free to open an issue for bugs and feature requests.

## License
STEP is released under the ['Add a license here' license]().

## Authors
* [Alex Rittler](https://www.linkedin.com/in/arittler) - *developer*

## Acknowledgements
* Won Chang - *research*
* Michael Stein - *research*
* Jiali Wang - *research*
* Rao Kotamarthi - *research*
* Elisabeth Moyer - *research*
* [Benjamin Kleeman](https://github.com/bkleeman) - *project maintenance & development*
* Emily Padston - *project management and guidance*
