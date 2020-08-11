# STEP (Storm Tracking and Evaluation Protocol)

STEP is a Python package that identifies, tracks, and computes physical characteristics of rainstorms given spatiotemporal precipitation data. The algorithms herein are implementations of those proposed by Chang et al. in [*Changes in Spatiotemporal Precipitation Patterns in Changing Climate Conditions*](https://geosci.uchicago.edu/~moyer/MoyerWebsite/Publications/Papers/Changes_Spatio-temporal_Precipitation_patterns.pdf), released by RDCEP under the [MIT License???](https://choosealicense.com/licenses/mit/). The functionality is as follows:

The identification algorithm divides the precipitation field at each time step into individual storms. The tracking algorithm builds rainstorm events evolving over time by tracking identified storms across consecutive time steps. Finally, the storm characteristics algorithm quantitatively describes individual storms in terms of duration, size, average intensity, and central location. In addition to these, the package provides a few simplistic plotting functions and examples to visualize the results of the first two algorithms and the associated precipitation data. A function to produce a histogram depicting the frequency of precipitation values is also provided to aid in finding an optimal precipitation threshold.

## Installation

 To install STEP, use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install STEP
```

UPDATE ONCE FINISHED

## Dependencies
|Name|Version|Home|Necessary in|Optional in
|--|--|--|--|--|
|Basemap|1.2.1|matplotlib.org/basemap|`plot_with_map`|`introduction`
|imageio|2.8.0|imageio.github.io|`plot_label2rgb` *`plot_storms`* `plot_with_map` |`introduction`
|Matplotlib|3.2.1|matplotlib.org|`plot_label2rgb` *`plot_storms`* `plot_with_map` |`introduction`
|netCDF4|1.5.3|unidata.github.io/netcdf4-python/netCDF4/index.html|**`none`**|`introduction`
|NumPy|1.18.5|numpy.org|**`all`**|**`none`**
|scikit-image|0.17.2|scikit-image.org|`colorlabel` *`identification`*  `introduction` `plot_label2rgb` *`tracking`*|**`none`**
|SciPy|1.4.1|scipy.org|*`identification`* *`tracking`*|`introduction`
|six|1.15.0|https://github.com/benjaminp/six|`colorlabel`|**`none`**

*Note: core functionality is italicized. All other files are examples or support examples.*

## Usage

Please see `introduction.py`, which provides a comprehensive introduction to package use. For further specificity, see the function signatures and usage tips for the main functionality listed below or call `help(`*`function`*`)` for information on these and functions called therein. Depending on the function, the latter may provide more function-specific information.

### Identification

Divide the precipitation field at each time step into individual storms by calling `identify` .

#### Signature

 - `data`: the precipitation data, given as an array of dimensions *Time x Rows x Cols*. To identify storms in a single time slice, reshape the array to dimensions (1, Rows, Cols).  
- `morph_structure`: the structural set used to perform morphological operations, given as an array.

`identify` returns an array of time slice maps with the dimensions of `data` containing individual storms labeled sequentially in each time slice.

#### Tips
 - When choosing a structural set for the associated morphological operations, it is highly likely that a disk of a particular radius should be used, as this structure ensures that a point in any direction from the segment being eroded or dilated has equal of chance of either. For more on creating a structural set, see the usage introduction `introduction.py` accompanying the package.
 - Since both erosion and deletion use the same structure, an increase in its size will likely lead to fewer large storms (since more of the map is being eroded) and greater connections between storms (as more storms will likely be connected in almost-connected component labeling). Likewise, a decrease in size adds up to more large storms and less connection between non-contiguous regions.
 - Also, for this reason, keep in mind that pursuing a particular connection (or lack thereof) in one portion of a map may lead to drastic changes not only with regards to other regions in the same time slice, but for the entire length of the run due to the structure's universal use.

### Tracking

Track rainstorm events over time by calling calling `track`.

#### Signature

- `labeled_maps`: the identified storms returned by the identification algorithm, given as an array of dimensions *Time x Rows x Cols*.  
- `precip_data`: the precipitation data corresponding to the identified storms, with the same dimensions as `labeled_maps`.  
- `tau`: the threshold at which a storm is considered similar enough to another to possibly be linked through time, given as a float.  
- `phi`: the constant to be used in computing similarity between storms, given as a float.
- `km`: the number of grid cells equivalent to 120km, given as a float.
- `test`: turn on/off optional testing printouts to help tune parameters, given as a boolean with default value False.
  
`track` returns an array with the dimensions of `labeled_maps` containing tracked storms labeled sequentially through time.

#### Tips

- Due to the complex nature of the computations used to track storms, please be aware that this algorithm requires a good deal of time to run and uses an immense amount of memory. For these reasons, it is highly recommended that runs of any substance be done on machines designed specifically for tasks of such computational weight.
 - Tracking precision is helped by smaller intervals between snapshots. The package was validated on data with 3 hour time step intervals, the same interval found in the paper.
 - Much of the success in tracking storms in predicated on effectively tweaking user-specified parameters *tau* and *phi* (after a successful identification run). The *tau* threshold is simply the value returned by the similarity measure deemed large enough to signify a match between storms. The constant *phi*, on the other hand, controls the output of the *similarity measure*. Directly, a greater constant yields a greater bias against points far apart in distance, and indirectly, this means similarity measures as a whole are reduced. As always, please see the paper for more information and calculation specifics.
 - As tracking may require a number of runs to fine tune, try tweaking parameters on a small temporal subset first. The tracking algorithm provides print statements to aid in interpreting the results of a run and finding optimal parameters. This feature can be toggled on by setting the optional parameter `test = True`.

### Quantification

Quantitatively describe individual storms in terms of duration, size, mean intensity, and central location by calling `quantify`.

#### Signature

- `tracked_storms`: the tracked storms returned by the tracking algorithm, given as an array of dimensions `Time x Rows x Cols`.  
- `precip_data`: the precipitation data corresponding to the tracked storms data, with the same dimensions as `tracked_storms`.  
- `lat_data`: the latitude data corresponding to each [*row*][*col*] location in `tracked_storms`, given as an array of dimensions *1 x Rows x Cols*.  
- `long_data`: the longitude data corresponding to each [*row*][*col*] location in `tracked_storms`, given as an array of dimensions *1 x Rows x Cols*.  
- `time_interval`: the period between temporal 'snapshots', given as a float. The user should interpret the duration results in terms of the unit of time implied here.  
- `pixel_size`: the length/width one grid cell represents in the data. The user should interpret the size and average intensity results in terms of the unit of distance implied here squared. 

`quantify` returns a tuple of size four containing the duration of each storm, as well as its size, mean intensity, and central location at each time step, in this order.

#### Tips

 - For each of the 'metric arrays' returned in the tuple excluding duration, the resulting data for storm *12* in time slice *7* can be found at [*7*][*12*]. For duration, simply specify the storm [*12*] for the storm's duration.
 - Excluding duration, if a storm is not present in a time slice, its metrics in that time slice will be reported as 0. 
 - To interpret results of the central location calculation, the user must familiarize themselves with the latitude and longitude data associated with the tracking results. Furthermore, producing an intensity plot will also be of great help. With these in hand, one may interpret the results of this calculation similarly to a traditional center of mass calculation (or the like), where positive values for both dimensions correspond to positive shifts away from an unweighted center in both latitude and longitude towards areas with more precipitation.

### Plotting

To visualize the results of the identification and tracking algorithms and the associated precipitation data, or produce a histogram depicting the frequency of precipitation values, the following can be called.

#### Signatures

`histogram` produces a histogram depicting the frequency of precipitation values over a set of time slices to aid in finding an optimal precipitation threshold which is shown and saved. 
- `data`: the data from which to construct the histogram.
- `bins`: the number of equal-width bins in the range. (From [Matplotlib](matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.hist.html).) 
- `bin_range`: the lower and upper range of the bins. (Same source as above.)

`histogram` returns None.

***

`show_save_intensities` produces an intensity plot for data containing precipitation intensities through time. A PNG image of each time slice is produced as well as a GIF of all time slices. All PNG's can be shown and saved, and the GIF can only be saved. 

- `data`: the storm data to be plotted, given as an array of dimensions *Time x Rows x Cols* containing precipitation data. To plot precipitation in a single time slice, reshape the array to dimensions (1, Rows, Cols).  
- `colormap`: the colormap given to the precipitation data, given as a LinearSegmentedColormap used by Matplotlib.
- `title`: the in-image title to give each image output, given as a string.
- `unit`: the unit of the precipitation values plotted.
-  `start_time`: the number of the first time slice in the data to be plotted, used in file naming and noting time in image outputs, where applicable, given as an integer. The default value is 0. 
- `show_save`: determines whether images produced are shown, saved, or both. The default argument is 'both', while 'show' only shows images and 'save' only saves them.
- `dpi`: the resolution in dots per inch, given as integer. The default value is 300.

`show_save_intensities` returns None.

***

`show_save_storms` produces a plot for data containing labeled storms, where each label is plotted to the same color throughout time slices. The plot also displays the number of the current time slice and optionally ticks as well for testing purposes.
- `data`: the storm data to be plotted, given as an array of dimensions *Time x Rows x Cols* containing labeled storms (fully-identified, tracked, or otherwise). To plot storms in a single time slice, reshape the array to dimensions (1, Rows, Cols).  
- `colors`: the colormap given to the storm labels. If colors is a LinearSegmentedColormap from Matplotlib, each label is given a unique color (when a cyclic colormap is not given), though color differentiation may suffer with longer runs. If colors is a Python list, labels are mapped by cycling through the list as a ListedColormap, which can lead to unfortunate color collisions. 
- Parameters `title`, `start_time`, `show_save`, and `dpi` are as above.
- `ticks`: the toggle for including ticks in the plot, given as a boolean. The default value is False. *Note: ticks and display of the current time slice may overlap in preview shown, but will not in saved image.*

`show_save_storms` returns None.

***


#### Tips

- The package provides several basic plotting options and examples. Those found in `plot_storms.py` are the callable visualization functions listed above. Those found under `examples` in `plot_with_map.py` and `plot_label2rgb.py` are examples whose purpose is explained below.
- Since users will likely want to produce custom plots, the functions therein are not very customizable through parameters and are only intended to provide the ability to visualize the results of these algorithms. Instead, the user may keep or remove features as they see fit in their own plots.
- On this topic, one feature will not be suitable for longer runs. Specifically, the use of a continuous colormap will lead to discernibility issues with longer runs. In is case, the user should give a list acting as a colormap, though this may of course run into its own issues when neighboring storms are given the same color, as this problem is optimized mostly on a plot by plot basis.
- `plot_labelrgb.py` is given as an example of how one might use scikit-image's *label2rgb* function to produce a plot similar to that done entirely through Matplotlib. There are two key points to note here: this example is given since the use of *pcolormesh* leads to a growth of 1 pixel or so around the edges of every connected component, most likely due to interpolation used by both it and *contourf*. *This alteration in display is not made in label2rgb.* That said, the current version of *label2rgb* has an unresolved bug related to mapping the same label in separate time slices to the same color, so *label2rgb* from scikit-image v12.3 is provided with the package in its original file `colorlabel.py` and used here. Alternatively, increasing *dpi* can help with this issue if storms seem to touch.
- `plot_with_map.py` provides an example for how to plot results of the core algorithms over a map. This structure can largely be used for the user's own work, but they will very likely need to provide a different map. See Basemap examples for this, as there are many good options available. Additionally, the colorbar displaying the currently active storms in each time slice is given as this may be of use, though it is impractical with a large number of storms.

## Methodology

*Note:* It is highly recommended to review this methodology or that which is available in the original publication and the accompanying supplemental materials before use. Since both the identification and tracking algorithms require user-specified parameters and are quite sensitive to these, reviewing this material, especially the "Usage Notes" accompanying each algorithm, will likely reduce time spent tuning for optimal results.

Please also see the associated paper for further information regarding reasoning behind these steps and the mathematics used herein.

UPDATE

### Identification

Identification of individual storms within each time slice is computed as follows in both high-level overview form and an implementation outline that closely follows the numbered steps in the code released to aid in understanding. Following these are some quick tips compiled for ease of use when getting started with the algorithm and making sense of its results!

#### Algorithm Overview

 1. Find all contiguous precipitation regions. That is, perform (fully) connected-component labeling.
 2. Classify a storm region as large if it has one or more remaining grid cells left after an erosion operation and small otherwise.
 3. For regions in the set of large regions:
     1. Find smoothed regions using an opening operation.
     2. Perform almost-connected-component labeling on them.
     3. Group the large regions based on the clustering results.
 4. For regions in the set of small regions:
	 1. Dilate each region.
	 2. If any larger regions overlap, add the region to the cluster that shares the largest number of grid cells.
	 3. Otherwise, perform almost-connected-component labeling for the regions not added to any clusters for the large regions.

### Tracking

Once the rainstorm segments for all time slices are identified, we link them through consecutive time steps to form rainstorm events evolving over time. The tracking of storm events is computed as follows, once again in both high-level overview form and an implementation outline that closely follows the numbered steps in the code released.

CHANGE TO FOLLOWS COMMENTS PROVIDED IN PACKAGE

#### Algorithm Overview

 1. At *t=0*, assign the rainstorm segments to different rainstorm events as their starting segments.
 2. For *t=1* onwards:
	 1. Link each segment to one of the segments in the previous step based on *similarity measure* and magnitude of *displacement vector*. More specifically, link the two if the following conditions are satisfied:
		 1. The shape of the two events are similar enough so that the value of the *similarity measure* between them exceeds a *tau* threshold of 0.05 in summer and 0.01 in winter **and**
		 2. The link does not result in too drastic a change of storm location in the opposite direction to its original movement. That is, we allow linkage only when the magnitude of the *displacement vector* of the two segments is less than (the equivalent of) 120 km (in grid cells) regardless of direction, **or** the angle between the *displacement vector* and the displacement between the segment in the previous time slice and its predecessor is less than 120 degrees.
	2. If no events satisfy the criteria, let the segment initialize a new rainstorm event as its starting segment.

#### Similarity Measure Overview

The implementation of the similarity measure calculation is a very technical and largely unintuitive one. For this reason, please also see the extensive comments provided in `tracking.py`. As is suggested there, working through a small example will likely be very helpful in understanding not only the specific implementation, but the idea behind it as well.

***

Due to the nature of the double summation, a vectorized solution is crucial here, though enormously memory heavy. Thus, in order to minimize this issue while maintaining some speed, the *similarity measure* is computed involving the union of cell locations in the two storms, since overlapping cells have no effect on similarity. This of course will lead to greater memory usage when there is no overlap, but has had a significantly positive effective when there is some and storms are very large, since this is where computation is normally derailed with a more straightforward implementation. 

 1. For each of the two storms, compute the relative weight for each grid cell, preserving the shape of the array.
 2. Again for each, find the coordinates of the non-zero precipitation data corresponding to each storm and compute their union, as overlapping cells will not effect our result.
 3. Reshape the location arrays into 1d arrays and compute their union.
 4. Place these coordinates in identical 1d arrays.
 5. Create two new arrays of weights, where each weight is added to the array only if its coordinates exist in the union of coordinates and placed where those coordinates exist the union of coordinates.
 6. Reshape both arrays of weights into 1d arrays, one as a column and one as a row, and compute their matrix multiplication.
 7. Similarly, compute the distances between each pair of coordinates in the coordinate arrays. 
 *(We now have two arrays where the distance between each relevant cell pairing of the two storms in the array of multiplied, relative weights can be found at the same location in the distance array.)*
 8. Compute the exponential involving *phi* element-wise on the array of distances.
 9. Compute the element-wise multiplication of this resulting array with the array of multiplied, relative weights.
 10. The summation of this array gives the *similarity measure* of the two storms.

CHANGE AND ADD HIGH LEVEL OVERVIEW
 
### Physical Characteristics
 
 Once rainstorm events have been tracked through time, we are able to characterize each individual rainstorm event with four metrics: duration, size, mean intensity, and central location. These are computed as follows.
 
#### Algorithm Overviews (and Code Outlines)
No explicit code outlines are given for this section, since the overviews virtually act as such. For more information on the implementation, see `quantification.py`.
##### Duration
 - Create a new dictionary.
 - Find all the storms in the tracked storm data.
 - Create a new array of length equal to the number of storms found. 
 - For each time slice:
	 1. Compute the storms that appear in that time slice.
	 2. For each storms in the set of all storms:
		 1. If that storm is in the set of storms that appear in this time slice:
			 1. If the storm is not already in the dictionary, add it with value 1.
			 2. Otherwise, increment the value found at the key equal to that storm.
 - For each key, value pair in the dictionary:
	1. If the key isn't the background:
		1. Set the value found at [*key*] of the array to the key's value in the dictionary.
 - Multiply each value of the array to be returned by the time interval. 
##### Size
 - Create an array with dimensions *number of time slices **x** number of storms*.
 - For each time slice:
	1. Find the storms that appear in it.
	2. For each storm that appears in this time slice:
		1. Compute the number of grid cells belonging to it.
		2. Place this result at the corresponding [*time*][*storm*] location in the array.
 - Multiply the number of grid cells by the specified grid cell size for the data.
##### Average intensity
 - Create an array with dimensions *number of time slices **x** number of storms*.
 - For each time slice:
	1. Find the storms that appear in it.
	2.  For each storm that appears in this time slice:
		1. Find and sum the precipitation belonging to the storm in the current time slice.
		2. Find the storm's average precipitation in this time slice.
		3.  Place this result at the corresponding [*time*][*storm*] location in the array.
##### Central location
 1. Create an array with dimensions *number of time slices **x** number of storms* to store the results of our computations, but of type object to allow us to store an array in each cell.
 2. Create arrays of x, y, and z values corresponding to the latitude and longitude data converted into the Cartesian grid in R<sup>3</sup>.
 3. For each time slice:
	1.  Find the storms that appear in it.
	2.  For each storm that appears in this time slice:
		1. Find the sum of the precipitation values belonging to the storm.
		2. Compute the intensity weighted averages corresponding to the grid in R<sup>3</sup> for the storm.
		3. Find the nearest point on Earth's surface.
		4. Place this result at the corresponding [*time*][*storm*] location in the array.

## Contributing

Changes are certainly welcome, as there are a good deal of complexity improvements to make on the implementation and functionality additions to build out related to the publication. If you would like to propose a change and/or note an error, please open an issue first to discuss what needs improvement (and, if applicable, how that might be accomplished).

### Future Work

Below are a list of generally useful ideas for future additions to STEP:

 - Adding the ability to use the computed metrics to find and visualize the spatial distribution of rainstorm characteristics, as covered in the publication.
 - Implementing a speed-up for the similarity measure computation. This could at least be done by dividing the calculation into subsets and summing their results.

## License
STEP is released under the [MIT License](https://choosealicense.com/licenses/mit/).
