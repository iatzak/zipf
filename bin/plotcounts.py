"""Plot word counts."""

import argparse
import pandas as pd


def main(args):
    """Run the command line program."""
    df = pd.read_csv(args.infile, header=None,
                     names=('word', 'word_frequency'))
    df['rank'] = df['word_frequency'].rank(ascending=False,
                                           method='max')
    scatplot = df.plot.scatter(x='word_frequency',
                               y='rank', loglog=True,
                               figsize=[12, 6],
                               grid=True,
                               xlim=args.xlim)
    scatplot.get_figure().savefig(args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        nargs='?', default='-',
                        help='Input CSV file name with word counts')
    parser.add_argument('-o', '--outfile',
                        type=str, default='plotcounts.png',
                        help='Output image file name')
    parser.add_argument('--xlim', type=float, nargs=2,
                        metavar=('XMIN', 'XMAX'),
                        default=None, help='X-axis limits')
    args = parser.parse_args()
    main(args)
