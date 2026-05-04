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
import warnings
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes

############################
# % FUNCTIONS
############################

def set_defaults(preset:str = 'paper') -> None:
    """
    Set matplotlib defaults that I always use.
    
    The selected preset optimises sizes for a particular purpose, e.g. 'paper' for use in paper, 'presentation' for use in presentation, 'inset' for a tiny inset. That kinda thing.
    """
    set_fontfamily()
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

def set_fontfamily(fontname="Roboto") -> None:
    """
    Set font family (so the way letters look) to given font.

    Yes, I know this is really easy in matplotlib, but I always forget how to do it.
    
    My personal default is **roboto** at the time of writing, since I read somewhere that this is easy to read on plots. Check that it is installed with 
    
    ``` 
    from matplotlib import font_manager
    sorted( font_manager.get_font_names() )
    ```
    """
    from matplotlib import font_manager
    fonts = sorted( font_manager.get_font_names() )
    if fontname in fonts:
        plt.rcParams["font.family"] = fontname
    else:
        print("Available Fonts in Matplotlib")
        print("-----------------------------")
        print("")
        for i in range(len(fonts)):
            print(fonts[i])
        raise ValueError(
            f"{fontname} is not available in matplotlib. Check for spelling (including capitalization) in list above. If font is installed but not in Matplotlib, try mplfonts package."
        )

def set_fonts(preset:str='paper',small:float=7, medium:float=9, big:float=11) -> None:
    """Set font-related settings. Use preset defaults (see set_defaults) or set things individually as required. **Does not change the font family, only the sizes**, check set_fontfamily for that."""
    plt.rcParams["svg.fonttype"] = "none" # This makes matplotlib text actually appear as text! Very important for editing in e.g. Inkscape.
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

def default_figsize(preset:str='paper', aspect_ratio=1) -> tuple[float,float]:
    """
    Returns the figure size this module is intended to work for. Note that this is the PLOTTING AREA, NOT THE CANVAS SIZE. So use with panel, not directly in a matplotlib plot!
    
    Parameters
    ----------
    preset: str, optional
        One of the presets also defined in set_defaults, e.g. 'paper', 'presentation', ...
    aspect_ratio: float, optional
        Change this number to make plot longer (in Y-direction) (make number higher) or shorten (make number smaller) then normal. Default is 1 (width=height). 

    Returns
    -------
    tuple[float,float]
        size of a single panel that will have the correct dimensions for all other parts of this default look to work.
    """
    if preset == 'paper':
        total_width = 40 # typically you have a total page width available of 160 mm, 40 mm is the natural size or a panel.
    elif preset == 'presentation':
        total_width = 200 # ppt slides are normally 28 x 15.75 cm (DEC 2025)
    elif preset == "inset":
        # not so easy but set a standard anyway so you have an aim at least
        total_width = 10
    else:
        raise NotImplementedError(f"{preset} is not implemented (yet) as a preset")
    panelwidth = total_width
    panelheight = aspect_ratio * panelwidth
    return (panelheight / 25.4,panelwidth / 25.4) # conver to inches!


def _parse_size(size_inch, size_mm):
    """Helper to get size in inches."""
    if size_inch and not size_mm:
        return np.array(size_inch)
    elif size_mm and not size_inch:
        return np.array(size_mm) / 25.4
    else:
        raise ValueError("Supply size in mm or inches, never both")


def panel(size_inch:None|tuple[float,float]=None, size_mm:None|tuple[float,float]=None) -> tuple[Figure, Axes]:
    """
    Create a Figure panel with a plotting area of the given size. The rest of the canvas will be scaled to fit figure labels etc. You can give the size in mm or inches.

    Parameters
    ----------
    size_inch : tuple[float,float]
        Size of the plotting area in INCHES (yes really)
    size_mm : tuple[float,float]
        Size of the plotting area in INCHES (yes really)

    Returns
    -------
    tuple[Figure, Axes]
        Figure and Axes objects normally returned by e.g. plt.subplots()

    Notes
    -----
    The inner workings of this are a bit magic to me, but it works, so don't ask too many questions.
    """
    size = _parse_size(size_inch, size_mm)
    fig = plt.figure(layout='compressed')          # 1. start with “rubber” canvas
    ax = fig.add_axes( (0, 0, 1, 1) )              # 2. Axes fills the *initial* figure
    # 3. fix the axes box to the required physical size
    ax.set_position(
        [0, 0, size[0] / fig.get_figwidth(), size[1] / fig.get_figheight()]
    )
    fig.set_size_inches(*fig.get_size_inches())    # 4. shrink-wrap the canvas
    return fig,ax


def panels_row(
    n: int,
    size_inch: None | tuple[float, float] = None,
    size_mm: None | tuple[float, float] = None,
    sharey: bool = True,
) -> tuple[Figure, list[Axes]]:
    """
    Create a figure with n side-by-side panels of equal plotting area size, touching edge-to-edge.

    Parameters
    ----------
    n : int
        Number of panels to place horizontally.
    size_inch : tuple[float,float]
        Size of each individual plotting area in INCHES (yes really).
    size_mm : tuple[float,float]
        Size of each individual plotting area in MILLIMETRES (yes really).
    sharey : bool
        Whether to share the y-axis between all panels. Default True.
    """
    size = _parse_size(size_inch, size_mm)
    panel_w, panel_h = size

    # Total figure size: n panels wide, 1 panel high
    fig_w = n * panel_w
    fig_h = panel_h

    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

    axes = []
    for i in range(n):
        rect = [i / n, 0, 1 / n, 1]  # [left, bottom, width, height] in figure fraction
        if i == 0:
            ax = fig.add_axes(rect)
            ax0 = ax
        else:
            ax = fig.add_axes(rect, sharey=ax0 if sharey else None)
        axes.append(ax)

    return fig, axes


def panels_col(
    n: int,
    size_inch: None | tuple[float, float] = None,
    size_mm: None | tuple[float, float] = None,
    sharex: bool = True,
) -> tuple[Figure, list[Axes]]:
    """
    Create a figure with n vertically stacked panels of equal plotting area size, touching edge-to-edge.

    Parameters
    ----------
    n : int
        Number of panels to place vertically.
    size_inch : tuple[float,float]
        Size of each individual plotting area in INCHES (yes really).
    size_mm : tuple[float,float]
        Size of each individual plotting area in MILLIMETRES (yes really).
    sharex : bool
        Whether to share the x-axis between all panels. Default True.

    Returns
    -------
    tuple[Figure, list[Axes]]
        Figure and list of Axes objects, top to bottom.
    """
    size = _parse_size(size_inch, size_mm)
    panel_w, panel_h = size

    # Total figure size: 1 panel wide, n panels high
    fig_w = panel_w
    fig_h = n * panel_h

    fig = plt.figure(figsize=(fig_w, fig_h))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

    axes = []
    for i in range(n):
        rect = [0, (n - 1 - i) / n, 1, 1 / n]  # bottom-to-top order
        if i == 0:
            ax = fig.add_axes(rect)
            ax0 = ax
        else:
            ax = fig.add_axes(rect, sharex=ax0 if sharex else None)
        axes.append(ax)

    return fig, axes


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
# % USEFULL SHORTCUTS
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
        fig,ax = panel(size_inch=size)
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

        fig,ax = panel(size_inch=size)

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


    def test_panels_row(savepath):
        """3 horizontal panels with shared y-axis."""
        fig, axes = panels_row(
            n=3, size_mm=(40, 40), sharey=True  # small panels to see the effect clearly
        )

        # Different x ranges, same y range — shared y should align them
        x_ranges = [(0, 10), (5, 15), (10, 20)]

        for i, ax in enumerate(axes):
            x = np.linspace(*x_ranges[i], 100)
            y = np.sin(x) + 0.3 * np.random.randn(100)
            ax.plot(x, y, color=f"C{i}", linewidth=2)
            ax.set_title(f"Panel {i+1}", fontsize=8)
            ax.set_xlabel("x")

        # Only leftmost y-label
        axes[0].set_ylabel("shared y")
        for ax in axes[1:]:
            ax.tick_params(labelleft=False)

        # Add vertical lines at panel boundaries to verify touching
        for ax in axes:
            ax.axvline(ax.get_xlim()[1], color="red", linestyle="--", alpha=0.3)

        fig.suptitle("panels_row: 3× horizontal, touching, sharey=True", fontsize=10)
        plt.savefig(savepath / "test_row.png", dpi=150)
        plt.show()


    def test_panels_col(savepath):
        """4 vertical panels with shared x-axis."""
        fig, axes = panels_col(n=4, size_mm=(60, 30), sharex=True)

        # Same x range, different y ranges — shared x should align them
        y_offsets = [0, 5, 10, 15]

        for i, ax in enumerate(axes):
            x = np.linspace(0, 10, 100)
            y = np.exp(-x / 3) + y_offsets[i] + 0.2 * np.random.randn(100)
            ax.plot(x, y, color=f"C{i+3}", linewidth=2)
            ax.set_ylabel(f"ch {i+1}", fontsize=8)

        # Only bottom x-label
        axes[-1].set_xlabel("shared x")
        for ax in axes[:-1]:
            ax.tick_params(labelbottom=False)

        # Add horizontal lines at panel boundaries to verify touching
        for ax in axes:
            ax.axhline(ax.get_ylim()[0], color="red", linestyle="--", alpha=0.3)

        fig.suptitle("panels_col: 4× vertical, touching, sharex=True", fontsize=10)
        plt.savefig(savepath / "test_col.png", dpi=150)
        plt.show()
    
    test_panels_row(savepath)
    test_panels_col(savepath)
