import argparse
import logging
import os
import sys
from distutils.dir_util import copy_tree

from harnic.compare import har_compare
from harnic.har import HAR
from harnic.helpers import stats_report, generate_artifacts
from harnic.utils import SPA_BASE

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

my_parser = argparse.ArgumentParser()

my_parser.add_argument('from_file', action='store', type=str,
                       help='First traffic file')

my_parser.add_argument('to_file', action='store', type=str,
                       help='Second traffic file')

args = my_parser.parse_args()


logger.info(f'Running version {os.environ.get("IMG_LABEL")}')
logger.info('Generating diffs...')
h1 = HAR(args.from_file)
h2 = HAR(args.to_file)
diff = har_compare(h1, h2)

out_dir = 'diff_' + os.path.basename(args.from_file) + '_' + os.path.basename(args.to_file)
copy_tree(SPA_BASE + "/build", out_dir)

generate_artifacts(diff, out_dir)

logger.info('Comparison artifacts generated: %r', out_dir)
logger.info(stats_report(diff))
