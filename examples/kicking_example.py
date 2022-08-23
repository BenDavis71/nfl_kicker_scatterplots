import numpy as np
import pandas as pd
from plots.kicker_scatter_plot import kicker_scatter_plot

# Import kicking data
df = pd.read_csv('/Users/bendavis/Documents/Football/field_goal_coordinates.csv.gz')

# Cut down to just Justin Tucker
df = df[(df['displayName'] == 'Justin Tucker')]

values = np.array(df[['x', 'y', 'made']])

title = 'Justin Tucker'
subtitle_1 = '2018-2020'
subtitle_2 = f'From {len(df)} kicks with tracking enabled'.format()
legend_title = 'Strike Rate'

kicker_scatter_plot(values)