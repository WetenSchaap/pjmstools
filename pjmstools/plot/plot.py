"""
Plotting functions

To make matplotlib plotting *consistent*.

This module works assuming you keep pics (approximately) the same size as you generate them - so no up/down-scaling!

Most important are:
    * Sets sane defaults for plot settings, like line thickness and ticklabelsize

    * squarify: function to make any plot square:
        >>> squarify(fig)
        [figure is now square]
    
    * Gives access to some small nice things, like extra line styles.
        >>> plt.plot(x,y,linestyle = linestyle_dict['loosely dashdotdotted'])

    * I would advise using tol-colors package to manage your colors.
"""
#%%
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes

############################
#% FUNCTIONS
############################

def set_defaults(preset:str = 'paper') -> None:
    """
    Set matplotlib defaults that I always use.
    
    The selected preset optimises sizes for a particular purpose, e.g. 'paper' for use in paper, 'presentation' for use in presentation, 'inset' for a tiny inset. That kinda thing.
    """
    set_fonts(preset=preset)
    set_line_properties(preset=preset)
    set_marker_properties(preset=preset)
    
    # Figure quality (in case of jpg/png/...)
    dpi = 300
    mpl.rcParams['figure.dpi'] = dpi
    mpl.rcParams['savefig.dpi'] = dpi # not sure if needed but cannot be too carefull

    # # Bounding box size (tight is really the only sane option, why is this not always on?!)
    # mpl.rcParams['savefig.bbox'] = "tight"
    # mpl.rcParams['savefig.pad_inches'] = 0.1

def set_fonts(preset:str='paper',small:float=7, medium:float=9, big:float=11) -> None:
    """Set font-related settings. Use preset defaults (see set_defaults) or set things individually as required."""
    if preset == 'manual':
        pass
    elif preset == 'paper':
        small = 7
        medium = 9
        big = 11
    elif preset == 'presentation':
        small = 10
        medium = 15
        big = 20
    elif preset == "inset":
        small = 7
        medium = 7
        big = 7
    else:
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset")
    plt.rc('font', size=small)          # controls default text sizes
    plt.rc('axes', titlesize=small)     # fontsize of the axes title
    plt.rc('axes', labelsize=medium)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=medium)   # fontsize of the tick labels
    plt.rc('ytick', labelsize=medium)   # fontsize of the tick labels
    plt.rc('legend', fontsize=medium)   # legend fontsize
    plt.rc('figure', titlesize=big)     # fontsize of the figure title

def set_line_properties(preset:str='paper', linewidth:float = 1.0) -> None:
    """
    Set properties of lines in the plot - meaning the axis frame, ticks, etc.

    Parameters
    ----------
    preset : str, optional
        _description_, by default 'paper'
    """
    if preset == 'manual':
        pass
    elif preset == 'paper':
        linewidth = 1.25
    elif preset == 'presentation':
        linewidth = 4
    elif preset == "inset":
        linewidth = 0.25
    else:
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset")
    plt.rc('axes', linewidth= linewidth)
    mpl.rcParams['xtick.major.width'] = linewidth
    mpl.rcParams['ytick.major.width'] = linewidth

def set_marker_properties(preset:str='paper', **kwargs) -> None:
    """
    Set properties of the plotted objects - lines, markers, etc.

    Parameters
    ----------
    preset : str, optional
        _description_, by default 'paper'
    **kwargs
        Contain other linewidth properties to set.
    """
    markeredgewidth = 0
    if preset == 'manual':
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset. sorry :/.")
    elif preset == 'paper':
        lw = 1.25
        markersize = 9
    elif preset == 'presentation':
        lw = 4
        markersize = 11
    elif preset == "inset":
        lw = 0.2
        markersize = 4
    else:
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset")
    plt.rc('lines', linewidth=lw)
    plt.rc('lines', markersize=markersize)
    plt.rc('lines', markeredgewidth=markeredgewidth)
    
def default_figsize(preset:str='paper', npanels:float=3, aspect_ratio:float = 1) -> tuple[float,float]:
    """
    Returns the figure size this module is intended to work for. Note that this is the PLOTTING AREA, NOT THE CANVAS SIZE. So use with panel, not directly in a matplotlib plot!
    
    Parameters
    ----------
    preset: str, optional
        One of the presets also defined in set_defaults, e.g. 'paper', 'presentation', ...
    npanels : float, optional
        Split the full width of the page/slide/whatever into this many individual panels (half panels also possible), by default 3.
    aspect_ratio: float, optional
        Change this number to elongate (make number higher) or shorten (make number smaller) then normal. Default is 1 (width=height). 

    Returns
    -------
    tuple[float,float]
        size of a single panel that will have the correct dimensions for all other parts of this default look to work.
    """
    if preset == 'paper':
        total_width = 160 # typically you have a total page width available of 160 mm
    elif preset == 'presentation':
        total_width = 280 # ppt slides are normally 28 x 15.75 cm (DEC 2025)
    elif preset == "inset":
        # not so easy I guess, typically the width of a normal figure I guess, which is 5-ish cm.
        total_width = 50
    else:
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset")
    panelwidth = total_width/npanels
    panelheight = aspect_ratio * panelwidth
    return (panelheight / 25.4,panelwidth / 25.4) # conver to inches!

def panel(size:tuple[float,float]) -> tuple[Figure, Axes]:
    """
    Create a Figure panel with a plotting area of the given size. The rest of the canvas will be scaled to fit figure labels etc.

    Parameters
    ----------
    size : tuple[float,float]
        Size of the plotting area in INCHES (yes really)

    Returns
    -------
    tuple[Figure, Axes]
        Figure and Axes objects normally returned by e.g. plt.subplots()
        
    Notes
    -----
    The inner workings of this are a bit magic to me, but it works, so don't ask too many questions.
    """
    fig = plt.figure(layout='compressed')          # 1. start with “rubber” canvas
    ax = fig.add_axes( (0, 0, 1, 1) )                # 2. Axes fills the *initial* figure
    # 3. fix the *axes* box to the required physical size
    ax.set_position([0, 0, size[0]/fig.get_figwidth(),size[1]/fig.get_figheight()])  # pyright: ignore[reportArgumentType]
    fig.set_size_inches(*fig.get_size_inches())    # 4. shrink-wrap the canvas
    return fig,ax

def squarify(fig:Figure) -> tuple[float, float]:
    """
    Make any matplotlib figure square.
    Just do all the setupe and end with:
        >>> squarify(fig)
    This should do the trick without worries.
    Returns the new size of the figure.
    """
    warnings.warn("Squarify is depricated - set fig size directly using panel()")
    w, h = fig.get_size_inches()
    if w > h:
        t = fig.subplotpars.top
        b = fig.subplotpars.bottom
        axs = h*(t-b)
        l = (1.-axs/w)/2
        fig.subplots_adjust(left=l, right=1-l)
    else:
        t = fig.subplotpars.right
        b = fig.subplotpars.left
        axs = w*(t-b)
        l = (1.-axs/h)/2
        fig.subplots_adjust(bottom=l, top=1-l)
    return (fig.get_figheight(), fig.get_figwidth())

############################
#% USEFULL SHORTCUTS
############################

# EXTRA LINESTYLES
linestyle_dict = {
    # defaults:
    'solid':                 'solid',      # Same as (0, ()) or '-'
    'dotted':                'dotted',    # Same as (0, (1, 1)) or '.'
    'dashed':                'dashed',    # Same as '--'
    'dashdot':               'dashdot',  # Same as '-.'
    
    'loosely dotted':        (0, (1, 10)),
    'dotted':                (0, (1, 1)),
    'densely dotted':        (0, (1, 1)),

    'loosely dashed':        (0, (5, 10)),
    'dashed':                (0, (5, 5)),
    'densely dashed':        (0, (5, 1)),

    'loosely dashdotted':    (0, (3, 10, 1, 10)),
    'dashdotted':            (0, (3, 5, 1, 5)),
    'densely dashdotted':    (0, (3, 1, 1, 1)),

    'dashdotdotted':         (0, (3, 5, 1, 5, 1, 5)),
    'loosely dashdotdotted': (0, (3, 10, 1, 10, 1, 10)),
    'densely dashdotdotted': (0, (3, 1, 1, 1, 1, 1))
}


############################
#% USEFULL TIPS
############################
## to get a specific color on a certain value in a color scale:
# cmap = mpl.cm.get_cmap('viridis') # or cmap = tc.colormaps['iridescent']
# rgba = cmap(0.5)
# print(rgba) # (0.127568, 0.566949, 0.550556, 1.0)
## Optionally, normalize: 
# norm = mpl.colors.Normalize(vmin=10.0, vmax=20.0)
# rgba = cmap(norm(15)) # norm results in 0.5
# print(rgba) # (0.127568, 0.566949, 0.550556, 1.0)
# see test below for clear example.


if __name__ == "__main__":
    """
    Quickly test plotting so you can see what a plot will look like. Running from the commandline will result in poorly squarified plots, so don't worry about that too much.
    """
    from pathlib import Path
    import numpy as np
    import tol_colors as tc
    savepath = Path(__file__).parent.parent.parent/'tests'/'imgdump'
    for preset in ["paper", "presentation", "inset"]:
        # DISCRETE DATA
        cset = tc.colorsets['bright']
        x = np.linspace(0,10*np.pi,100)
        y = list()
        
        set_defaults(preset)
        size = default_figsize(preset)
        fig,ax = panel(size=size)
        for i in range(4):
            y.append( np.sin(x*(i+1)*0.1) )
            ax.plot(
                x,
                y[i],
                '-',
                color = cset[i],
            )
        plt.show()
        fig.savefig(savepath/f"{preset}.png",dpi=150,bbox_inches='tight')
        
        # CONT DATA
        datasets = 10
        cset = tc.colormaps['iridescent']
        norm = mpl.colors.Normalize(vmin=0, vmax=datasets)
        x = np.linspace(0,10*np.pi,15)
        y = list()

        fig,ax = panel(size=size)

        for i in range(datasets):
            y.append( np.sin(x*(i+1)*0.1) )
            rgba = cset(norm(i))
            ax.plot(
                x,
                y[i],
                's',
                color = rgba,
            )
        plt.show()