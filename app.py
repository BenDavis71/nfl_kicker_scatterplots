import streamlit as st
import numpy as np
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d


@st.cache(allow_output_mutation=True)
def get_data():
    session = requests.Session()
    session.auth = (st.secrets.username, st.secrets.password)
    url = st.secrets.url

    download = session.get(url).content
    return pd.read_csv(io.StringIO(download.decode('utf-8')))


@st.cache(allow_output_mutation=True)
def get_headshots():
    return pd.read_csv('https://github.com/nflverse/nflverse-data/releases/download/players/players.csv')


def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, facecolor='black', edgecolor='black', alpha=None, **kwargs):
    x, y, z = xyz
    if zdir == "y":
        xy1, z1 = (x, z), y
    elif zdir == "x":
        xy1, z1 = (y, z), x
    else:
        xy1, z1 = (x, y), z

    text_path = TextPath((0, 0), s, size=size, usetex=usetex) # prop=fp if required
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])

    p1 = PathPatch(trans.transform_path(text_path), facecolor=facecolor, edgecolor=edgecolor, fill=True)
    p1.set_alpha(alpha)  # Very important - needed so alpha is respected
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)


def plot_field_3d(ax,
                   field_color='white',
                   outline_color='#595959',
                   marking_color='#595959',
                   goalpost_color='slategray',
                   yard_line_number_color='lightgrey',):

    LINEWIDTH = 3

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

    for dist in range(5, FIELD_LENGTH, 5):
        # Plot those lines that are every 5 yards
        ax.plot([INBOUND_LINE_END_DISTANCE - FIELD_WIDTH / 2, -INBOUND_LINE_END_DISTANCE + FIELD_WIDTH / 2], [dist, dist], 0, c=marking_color, alpha=0.2, lw=1)

        # Plot numbers indicating yard lines onto field
        if dist % 10 == 0:
            if dist <= FIELD_LENGTH // 2:
                text3d(ax, (-YARD_LINE_NUMBER_DISTANCE + FIELD_WIDTH / 2, dist - 1.9, 0),
                                       str(dist),
                                      zdir="z", size=3, usetex=False, angle=-67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

                text3d(ax, (YARD_LINE_NUMBER_DISTANCE - FIELD_WIDTH / 2, dist + 1.9, 0),
                                      str(dist),
                                      zdir="z", size=3, usetex=False, angle=67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

            elif dist < FIELD_LENGTH:
                text3d(ax, (-YARD_LINE_NUMBER_DISTANCE + FIELD_WIDTH / 2, dist - 2, 0),
                                      str(FIELD_LENGTH - dist),
                                      zdir="z", size=3, usetex=False, angle=-67.55,  # np.pi,
                                      facecolor=yard_line_number_color, edgecolor=yard_line_number_color)

                text3d(ax, (YARD_LINE_NUMBER_DISTANCE - FIELD_WIDTH / 2, dist + 2, 0),
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


def kicker_scatter_plot(values, azim, elev, x_bound, y_bound, z_bound):
    fig = plt.figure()
    fig.set_size_inches(8, 5)
    fig.subplots_adjust(left=0,
                        right=1,
                        bottom=-.4,
                        top=2)  # Get rid of some excess whitespace - adjust to taste

    ax = plt.gca(projection='3d')

    ax.view_init(elev=elev, azim=azim)

    # Edit these in order to pan the camera
    ax.set_xlim3d([-x_bound, x_bound])
    ax.set_ylim3d([y_bound - 30, y_bound])
    ax.set_zlim3d([0, z_bound])

    # No ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_box_aspect(
        (2 * x_bound, 30, z_bound))  # max - min for each axis

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
    return fig


# Main
st.title('NFL Kicker Tracking Scatter Plots')

# Import kicking data
df = get_data()

# Select kicker
kicker = st.selectbox("Kicker", sorted(set(df['displayName'].tolist())))

# Cut down to selected kicker
df = df[df['displayName'] == kicker]

# Get and display kicker headshot in the center
headshot_df = get_headshots()
try:
    left, middle = st.columns((2.28, 5))
    with middle:
        st.image(headshot_df[headshot_df['display_name'] == kicker]['headshot'].reset_index(drop=True)[0], width=250)
except:
    pass  # If headshot not available

# Transform dataframe into an array in order to pass to function
values = np.array(df[['x', 'y', 'made']])

# Include sidebar for adjusting 3D view
with st.sidebar:
    st.title('Camera Sliders')
    azim = st.slider("Rotation", 0, 360, 0, 1) + 90
    elev = st.slider("Angle", 0, 90, 12, 1)
    x_bound = 100 - st.slider("Zoom", 0, 99, 80, 1)
    y_bound = st.slider("Pan", 0, 99, 15, 1)
    z_bound = st.slider("Height", 0, 99, 25, 1)

# Create and output figure
fig = kicker_scatter_plot(values, azim, elev, x_bound, y_bound, z_bound)
buf = io.BytesIO()
fig.savefig(buf, format="png")
st.image(buf)

# Description of stats
st.write(f"{kicker} made {df['made'].sum()} out of {df['made'].count()} kicks with tracking data in the 2018-2020 seasons")


st.markdown('___')
st.markdown('Created by [Ben Davis](https://github.com/BenDavis71/)')