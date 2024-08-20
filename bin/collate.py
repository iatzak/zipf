"""
Combine multiple word count CSV-files
into a single cumulative count.
"""

import csv
import argparse
from collections import Counter
import logging

import utilities as util


ERRORS = {
    'not_csv_suffix': '{fname}: Filename must end in .csv',
}


def update_counts(reader, word_counts):
    """Update word counts with data from another reader/file."""
    for word, count in csv.reader(reader):
        word_counts[word] += int(count)


def main(args):
    """Run the command line program."""
    log_level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level,
                        filename=args.logfile)
    word_counts = Counter()
    logging.info('Processing files...')
    for fname in args.infiles:
        try:
            logging.debug(f'Reading in {fname}...')
            if fname[-4:] != '.csv':
                msg = ERRORS['not_csv_suffix'].format(fname=fname)
                raise OSError(msg)
            with open(fname, 'r') as reader:
                logging.debug('Computing word counts...')
                update_counts(reader, word_counts)
        except FileNotFoundError:
            logging.warning(f'{fname} not processed: file not found')
        except PermissionError:
            logging.warning(f'{fname} not processed: unsufficient permissions')
        except Exception as error:
            logging.warning(f'{fname} not processed: {error}')
    util.collection_to_csv(word_counts, num=args.num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', type=str, nargs='*',
                        help='Input file names')
    parser.add_argument('-n', '--num', type=int, default=None,
                        help='Output n most frequent words')
    parser.add_argument('-v', '--verbose', default=None,
                        action=argparse.BooleanOptionalAction,
                        help='Set logging level to DEBUG')
    parser.add_argument('-l', '--logfile', type=str,
                        default='collate.log',
                        help='Specify filename of log file')
    args = parser.parse_args()
    main(args)
