from __future__ import division

import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import soundfile as sf
import argparse
import pickle


def wavplot(
    data,
    type='bar',
    num_bars=200,
    width=1000,
    height=200,
    dpi=50,
    color_max='#E8C18A',
    color='#ED8C01',
    no_max=False,
):
    """Render a nice looking envelope waveform

    Parameters
    ----------
    data : array_like
        The input audio data
    type : string
        The type of plot to render
    num_bars : int
        Number of bars to plot
    width : float
        Width of output image in inches
    height : float
        Height of output image in inches
    dpi : float
        Dots per inch
    color : string
        Color to use.

    Returns
    -------
    f : figure
        The resulting matplotlib figure

    """
    data = data.copy()
    # Atleast 2D, last dimension is added
    data = np.atleast_2d(data.T).T

    plt.rcdefaults()

    f, ax = plt.subplots(
        1,
        1,
        sharex=True,
        figsize=(width/dpi, height/dpi),
        dpi=dpi
    )

    num_samples = len(data)

    frame_length = num_samples // num_bars

    # samples, channels
    data = data[:num_bars * frame_length, :]

    # blocks, samples, channels
    data = data.T.reshape(
        (data.shape[1], num_bars, frame_length)
    ).transpose((1, 2, 0))

    x_mean = np.sqrt(np.mean(data ** 2, axis=(1, 2)))
    x_max = np.sqrt(np.mean(data ** 2, axis=(1, 2)))

    if not no_max:
        maxv = np.max(x_max)
    else:
        maxv = np.max(x_mean)

    x_mean /= maxv
    x_mean = np.maximum(x_mean, .001)

    x_max /= maxv
    x_max = np.maximum(x_max, .001)

    ax.set_xlim([0, num_bars+5])
    ax.set_ylim([-1, 1])
    if type == 'bar':
        if not no_max:
            ax.bar(
                np.arange(num_bars),
                2*x_max,
                bottom=-x_max,
                color=color_max,
                edgecolor='#eeeeee',
                linewidth=0.5,
                width=1
            )

        ax.bar(
            np.arange(num_bars),
            2*x_mean,
            bottom=-x_mean,
            color=color,
            edgecolor='#eeeeee',
            linewidth=0.5,
            width=1
        )

    plt.axis('off')
    return f


def main(args=None):
    # cmd line args
    parser = argparse.ArgumentParser(
        description='Read Wav and plot nice waveform'
    )
    parser.add_argument(
        '--bars', default=200,
        help="Number of bars", type=int,
    )
    parser.add_argument(
        '--width', default=1000,
        help="Output image width in inches", type=float,
    )
    parser.add_argument(
        '--height', default=200,
        help="Output image height in inches", type=float,
    )
    parser.add_argument(
        '--dpi', default=50,
        help="Output image dpi", type=float,
    )
    parser.add_argument(
        '--color', default='#ED8C01',
        help="Color of plot. May be a hexstring (#ff0000) or a comma "
             "separated list of float values between 0 and 1 "
             "(1.0,0.0,0.0,0.8), the optional last value denoting the alpha "
             "value.",
    )
    parser.add_argument(
        '--color-max',
        help="Color of maxima. Alpha transparent value of --color by default.",
    )
    parser.add_argument(
        '--no-max', action='store_true', help="Disable rendering peaks",
    )
    parser.add_argument(
        '--pickle', action='store_true', help="Load file as Python pickle",
    )
    parser.add_argument('datafile')
    parser.add_argument('image')

    args = parser.parse_args(args)

    try:
        args.color = [float(x) for x in args.color.split(',')]
    except ValueError:
        pass

    try:
        args.color_max = [float(x) for x in args.color_max.split(',')]
    except (ValueError, AttributeError):
        pass

    if args.color_max is None:
        args.color_max = matplotlib.colors.colorConverter.to_rgba(
            args.color, alpha=0.35
        )

    with open(args.datafile, 'rb') as dfile:
        if args.pickle:
            data = pickle.load(dfile)
        else:
            data, _ = sf.read(dfile)

    f = wavplot(
        data,
        num_bars=args.bars,
        width=args.width,
        height=args.height,
        dpi=args.dpi,
        color_max=args.color_max,
        color=args.color,
        no_max=args.no_max,
    )
    f.savefig(args.image, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    main(sys.args)
