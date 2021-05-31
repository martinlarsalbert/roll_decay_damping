import matplotlib.pyplot as plt
import pandas as pd

def plot(data:pd.DataFrame, y='phi', ax=None, **kwargs):

    if ax is None:
        fig,ax=plt.subplots()

    data.plot(y=y, ax=ax, **kwargs);

    ax.set_xlabel(r'time $[s]$')
    ax.grid(True)

    if y is 'phi':
        ax.set_ylabel(r'Roll angle $\phi$ $[rad]$')
    elif y is 'phi1d':
        ax.set_ylabel(r'Roll angle $\dot{\phi}$ $[rad/s]$')
    elif y is 'phi2d':
        ax.set_ylabel(r'Roll angle $\ddot{\phi}$ $[rad/s^2]$')

    return ax
