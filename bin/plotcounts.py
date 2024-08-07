"""Plot word counts."""

import yaml
import argparse
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
import matplotlib as mpl
import matplotlib.pyplot as plt


def nlog_likelihood(beta, counts):
    """Log-likelihood function."""
    likelihood = -np.sum(np.log((1/counts)**(beta - 1)
                         - (1/(counts + 1))**(beta - 1)))
    return likelihood


def get_power_law_params(word_counts):
    """Get the power law parameters.

    Moreno-Sanchez et al (2016) define alpha (eq. 1),
    beta (eq. 2) and the maximum likelihood estimation (mle)
    of beta (eq. 6).
    https://doi.org/10.1371/journal.pone.0147073
    """
    assert type(word_counts) == np.ndarray, 'Input must be a numerical (numpy) array of word counts'
    mle = minimize_scalar(nlog_likelihood,
                          bracket=(1 + 1e-10, 4),
                          args=word_counts,
                          method='brent')
    beta = mle.x
    alpha = 1 / (beta - 1)
    return alpha


def set_plot_params(param_file):
    """Set the matplotlib parameters."""
    if param_file:
        with open(param_file, 'r') as reader:
            param_dict = yaml.load(reader,
                                   Loader=yaml.BaseLoader)
    else:
        param_dict = {}
    for param, value in param_dict.items():
        mpl.rcParams[param] = value


def plot_fit(curve_xmin, curve_xmax, max_rank, alpha, ax):
    """Plot the power law curve that was fitted to the data.

    Args:
        curve_xmin (float): Minimum x-bound for fitted curve
        curve_xmax (float): Maximum x-bound for fitted curve
        max_rank (int): Maximum word frequency rank
        alpha (float): Estimated alpha parameter for the power law
        ax (matplotlib.axes): Scatter plot to which the power curve will be added
    """
    xvals = np.arange(curve_xmin, curve_xmax)
    yvals = max_rank * (xvals**(-1/alpha))
    ax.loglog(xvals, yvals, color='grey')


def save_configuration(fname, params):
    """Save configuration to a file."""
    with open(fname, 'w') as reader:
        yaml.dump(params, reader)


def main(args):
    """Run the command line program."""
    set_plot_params(args.plotparams)
    if args.style:
        plt.style.use(args.style)
    if args.saveconfig:
        save_configuration(args.saveconfig, mpl.rcParams)
        return
    df = pd.read_csv(args.infile, header=None,
                     names=('word', 'word_frequency'))
    df['rank'] = df['word_frequency'].rank(ascending=False,
                                           method='max')
    ax = df.plot.scatter(x='word_frequency',
                         y='rank', loglog=True,
                         figsize=[12, 6],
                         grid=True,
                         xlim=args.xlim)

    word_counts = df['word_frequency'].to_numpy()
    alpha = get_power_law_params(word_counts)
    print(f"alpha: {alpha}")

    # Since the ranks are already sorted, we can take the last
    # one instead of computing which row has the highest rank
    max_rank = df['rank'].to_numpy()[-1]    

    # Use the range of the data as the boundaries
    # when drawing the power law curve
    curve_xmin = df['word_frequency'].min()
    curve_xmax = df['word_frequency'].max()

    plot_fit(curve_xmin, curve_xmax, max_rank, alpha, ax)
    ax.figure.savefig(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        nargs='?', default='-',
                        help='Word count csv file name')
    parser.add_argument('-o', '--outfile',
                        type=str, default='plotcounts.png',
                        help='Output image file name')
    parser.add_argument('--xlim', type=float, nargs=2,
                        metavar=('XMIN', 'XMAX'),
                        default=None, help='X-axis limits')
    parser.add_argument('--plotparams', type=str, default=None,
                        help='matplotlib parameters (YAML file)')
    parser.add_argument('--style', type=str, default=None,
                        nargs='*', choices=plt.style.available,
                        help='Matplotlib plot style')
    parser.add_argument('--saveconfig', type=str, default=None,
                        help='Save configuration to file')
    args = parser.parse_args()
    main(args)
