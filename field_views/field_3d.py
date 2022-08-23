from matplotlib import colors
import plotting_utils


def plot_field_3d(ax,
                   field_color='white',
                   outline_color='#595959',
                   marking_color='#595959',
                   goalpost_color='slategray',
                   yard_line_number_color='lightgrey',):

    """ Plots an NFL football field to regulation dimensions in yards
    Origin (0,0) is the middle of one of the goal lines

    ----------
    ax: A matplotlib axis where ax = plt.gca(projection='3d')
        The 3D axes to plot on.
    field_color: A matplotlib named color string OR an RGBA (0-1) tuple
        The color of the football. Not configurable at the moment
    outline_color: Any valid matplotlib color
        The color of the boundaries of the field (sidelines and back of endzones)
    marking_color: Any valid matplotlib color
        The color of the field markings (goal line, hashmarks, etc)
    marking_color: Any valid matplotlib color
        The color of the pitch line markings
    goalpost_color: Any valid matplotlib color
        The color of the goalpost.
    yard_line_number_color: Any valid matplotlib color
        The color of the yard line numbers

    Returns
    -------
    matplotlib.axes.Axes"""

    X_BOUND = 20
    Y_BOUND = 15
    Z_BOUND = 25
    LINEWIDTH = 3
    BEHIND_GOALLINE_Y_LIMIT = -25

    ax.view_init(elev=12, azim=90)

    FIELD_LENGTH = 100
    FIELD_WIDTH = 53 + 1/3
    ENDZONE_LENGTH = 10

    CROSSBAR_HEIGHT = 3 + 1/3
    CROSSBAR_WIDTH = 6 + 1/6
    GOALPOAST_HEIGHT = 10

    HASHMARK_LENGTH = 2/3
    INBOUND_LINE_START_DISTANCE = 8/9
    INBOUND_LINE_END_DISTANCE = 2/9
    YARD_LINE_NUMBER_DISTANCE = 12


    min_h = 0  # Z height to plot court lines - 99% use cases will be ground level i.e. 0

    # Edit these in order to pan the camera
    ax.set_xlim3d([-X_BOUND, X_BOUND])
    ax.set_ylim3d([BEHIND_GOALLINE_Y_LIMIT, Y_BOUND])
    ax.set_zlim3d([0, Z_BOUND])

    # Plot sidelines
    ax.plot([-FIELD_WIDTH / 2, -FIELD_WIDTH / 2], [-ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH],
            min_h, c=outline_color, lw=0.5, zorder=1)
    ax.plot([FIELD_WIDTH / 2, FIELD_WIDTH / 2], [-ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH],
            min_h, c=outline_color, lw=0.5, zorder=1)

    # Plot backs of endzones
    ax.plot([-FIELD_WIDTH / 2, FIELD_WIDTH / 2],
            [FIELD_LENGTH + ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH],
            min_h, c=outline_color, lw=0.5, zorder=1)
    ax.plot([-FIELD_WIDTH / 2, FIELD_WIDTH / 2],
            [-ENDZONE_LENGTH, -ENDZONE_LENGTH],
            min_h, c=outline_color, lw=0.5, zorder=1)

    # Plot goal lines
    ax.plot([-FIELD_WIDTH / 2, FIELD_WIDTH / 2], [0, 0],
            min_h, c=marking_color, zorder=1)
    ax.plot([-FIELD_WIDTH / 2, FIELD_WIDTH / 2], [FIELD_LENGTH, FIELD_LENGTH],
            min_h, c=marking_color, zorder=1)

    # Plot those lines that are 2 yards out from the goal line
    ax.plot([-.5, .5], [2, 2],
            min_h, c=marking_color, alpha=0.2, lw=1, zorder=1)
    ax.plot([-.5, .5], [FIELD_LENGTH - 2, FIELD_LENGTH - 2],
            min_h, c=marking_color, alpha=0.2, lw=1, zorder=1)

    # Draw goalpost bottom bar
    x = [0, 0]
    y = [-ENDZONE_LENGTH, -ENDZONE_LENGTH]
    z = [0, CROSSBAR_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw crossbar
    x = [-CROSSBAR_WIDTH / 2, CROSSBAR_WIDTH / 2]
    y = [-ENDZONE_LENGTH, -ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, CROSSBAR_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw goalpost other bars
    x = [CROSSBAR_WIDTH / 2, CROSSBAR_WIDTH / 2]
    y = [-ENDZONE_LENGTH, -ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, GOALPOAST_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    x = [-CROSSBAR_WIDTH / 2, -CROSSBAR_WIDTH / 2]
    y = [-ENDZONE_LENGTH, -ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, GOALPOAST_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw other goalpost bottom bar
    x = [0, 0]
    y = [FIELD_LENGTH + ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH]
    z = [0, CROSSBAR_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw other crossbar
    x = [-CROSSBAR_WIDTH / 2, CROSSBAR_WIDTH / 2]
    y = [FIELD_LENGTH + ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, CROSSBAR_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw other goalpost other bars
    x = [CROSSBAR_WIDTH / 2, CROSSBAR_WIDTH / 2]
    y = [FIELD_LENGTH + ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, GOALPOAST_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    x = [-CROSSBAR_WIDTH / 2, -CROSSBAR_WIDTH / 2]
    y = [FIELD_LENGTH + ENDZONE_LENGTH, FIELD_LENGTH + ENDZONE_LENGTH]
    z = [CROSSBAR_HEIGHT, GOALPOAST_HEIGHT]
    ax.plot(x, y, z, color=goalpost_color, linewidth=LINEWIDTH, zorder=1000)

    # Draw the field's surface
    # Might add realistic colors in the future (green field, yellow goal posts, etc)
    # x = [FIELD_WIDTH / 2,
    #      -FIELD_WIDTH / 2,
    #      -FIELD_WIDTH / 2,
    #      FIELD_WIDTH / 2]
    # y = [FIELD_LENGTH + ENDZONE_LENGTH,
    #      FIELD_LENGTH + ENDZONE_LENGTH,
    #      -ENDZONE_LENGTH,
    #      -ENDZONE_LENGTH]
    # z = [0, 0, 0, 0]
    # verts = [list(zip(x, y, z))]
    # ax.add_collection3d(art3d.Poly3DCollection(verts,
    #                                            facecolors='field_color',
    #                                            alpha=.7,
    #                                            zorder=0))

    # Get rid of colored axes planes
    # First remove fill
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = True

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    # We accept either RGBA (0,1) or matplotlib named color string
    if isinstance(field_color, str):
        ax.w_zaxis.set_pane_color(colors.to_rgba(field_color, 1))
    else:
        ax.w_zaxis.set_pane_color(field_color)

    # Remove grid
    ax.grid(False)

    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # Transparent spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # No ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_box_aspect(
        (2 * X_BOUND, Y_BOUND - BEHIND_GOALLINE_Y_LIMIT, Z_BOUND))  # max - min for each axis

    for dist in range(5, FIELD_LENGTH, 5):
        # Plot those lines that are every 5 yards
        ax.plot([INBOUND_LINE_END_DISTANCE - FIELD_WIDTH / 2, -INBOUND_LINE_END_DISTANCE + FIELD_WIDTH / 2], [dist, dist], 0, c=marking_color, alpha=0.2, lw=1)

        # Plot numbers indicating yard lines onto field
        if dist % 10 == 0:
            if dist <= FIELD_LENGTH // 2:
                plotting_utils.text3d(ax, (-YARD_LINE_NUMBER_DISTANCE + FIELD_WIDTH / 2, dist - 1.9, 0),
                                       str(dist),
                                      zdir="z", size=3, usetex=False, angle=-67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

                plotting_utils.text3d(ax, (YARD_LINE_NUMBER_DISTANCE - FIELD_WIDTH / 2, dist + 1.9, 0),
                                      str(dist),
                                      zdir="z", size=3, usetex=False, angle=67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

            elif dist < FIELD_LENGTH:
                plotting_utils.text3d(ax, (-YARD_LINE_NUMBER_DISTANCE + FIELD_WIDTH / 2, dist - 2, 0),
                                      str(FIELD_LENGTH - dist),
                                      zdir="z", size=3, usetex=False, angle=-67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

                plotting_utils.text3d(ax, (YARD_LINE_NUMBER_DISTANCE - FIELD_WIDTH / 2, dist + 2, 0),
                                      str(FIELD_LENGTH - dist),
                                      zdir="z", size=3, usetex=False, angle=67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

    # Plot hashmarks and inbound lines
    for dist in range(1, FIELD_LENGTH):
        if dist % 5 != 0:
            ax.plot([-HASHMARK_LENGTH - CROSSBAR_WIDTH / 2, -CROSSBAR_WIDTH / 2], [dist, dist],
                    0, c=marking_color, alpha=0.2, lw=1)
            ax.plot([HASHMARK_LENGTH + CROSSBAR_WIDTH / 2, CROSSBAR_WIDTH / 2], [dist, dist],
                    0, c=marking_color, alpha=0.2, lw=1)

            ax.plot([INBOUND_LINE_END_DISTANCE - FIELD_WIDTH / 2, INBOUND_LINE_START_DISTANCE - FIELD_WIDTH / 2], [dist, dist],
                    0, c=marking_color, alpha=0.2, lw=1)
            ax.plot([-INBOUND_LINE_END_DISTANCE + FIELD_WIDTH / 2, -INBOUND_LINE_START_DISTANCE + FIELD_WIDTH / 2], [dist, dist],
                    0, c=marking_color, alpha=0.2, lw=1)
