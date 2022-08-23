"""
Plotting template for a football field with overlaid 2D scatter plot based on a specified values array
"""

import matplotlib.pyplot as plt
from field_3d import plot_field_3d
from utilities.plotting_utils import *


def kicker_scatter_plot(values):

    """ Plots a scatter plot overlaid on wicket_3d front view, using a specified values array for square shading

    ----------
    xy: A 2d array
        The x and y coordinates of the delivery pitching locations
    values: A 1d array
        The values which will determine the heatmap zone shading
    title: A string
        The plot title
    subtitle_1: A string
        The plot's 1st subtitle
    subtitle_2: A string
        The plot's 2nd subtitle
    legend_title: A string
        The title of the value legend
    min_balls: An integer
        The minimum number of balls used for each heatmap zone. If not met the zone is not displayed
    cmap: Any valid matplotlib named colormap string
        The color map used for the heatmap shading
    measure: string
        The measurement type used for the values. Can be:
        "strike_rate" - Strike Rate, value multiplied by 100
        "economy" - Economy, value multiplied by 6
        Any other value - No transformation applied

    Returns
    -------
    matplotlib.axes.Axes"""

    fig = plt.figure()
    fig.set_size_inches(8, 5)
    fig.subplots_adjust(left=0,
                        right=1,
                        bottom=-.4,
                        top=2)  # Get rid of some excess whitespace - adjust to taste

    ax = plt.gca(projection='3d')

    plot_field_3d(ax)

    for x, y, made in values:
        if made:
            text3d(ax, (x - 2/3, y, 0),
                   '⊙',
                   zdir="z", size=1.75, alpha=.6,
                   facecolor='teal', edgecolor='#75ffff')
        else:
            text3d(ax, (x - 2/3, y, 0),
                          'x',
                          zdir="z", size=1.75, alpha=.4,
                          facecolor='red', edgecolor='red')


    plt.show()