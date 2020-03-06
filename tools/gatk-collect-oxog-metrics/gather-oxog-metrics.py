#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import json
from glob import glob
import tempfile
import re

om = __import__('gatk-collect-oxog-metrics')


def main():
    parser = argparse.ArgumentParser(description='GATK CollectOxoGMetrics')

    parser.add_argument('-m', dest='metrics_tars', type=str,
                        help='Input OxoG Metrics Tarballs', required=True, nargs='+')

    args = parser.parse_args()

    basename = ''
    for m in args.metrics_tars:
        # 0000-8f879c15-14da-593d-bb76-db866f81ab3a.6.20190927.wgs.grch38.bam.oxog_metrics.txt
        untar_cmd = f'tar xf {m}'
        om.run_cmd(untar_cmd)
        basename = os.path.basename(m)

    basename = re.sub(r'^\d{4}\-', '', basename)
    basename = re.sub(r'\.oxog_metrics\.tgz$', '', basename)

    # find first JSON file and load extra_info
    with open(glob('*.extra_info.json')[0]) as j:
        extra_info = json.load(j)

    # remove all JSONs
    for f in glob('*.extra_info.json'):
        os.remove(f)

    # create a merged oxog metrics file
    merged_metrics = tempfile.NamedTemporaryFile(delete=False)

    first = True
    for m in glob('*.oxog_metrics.txt'):
        with open(m, 'rb') as r:
            for line in r:
                if line.startswith(b'#') or \
                        len(line.strip()) == 0 or \
                        (line.startswith(b'SAMPLE_ALIAS') and not first):
                    continue
                merged_metrics.write(line)
                first = False

    merged_metrics.close()

    oxoQ_score = om.get_oxoQ(merged_metrics.name)
    extra_info['oxoQ_score'] = float('%.4f' % oxoQ_score) if oxoQ_score is not None else None
    os.remove(merged_metrics.name)

    with open("%s.extra_info.json" % basename, 'w') as f:
        f.write(json.dumps(extra_info, indent=2))

    cmd = 'mkdir -p out && tar czf out/%s.oxog_metrics.tgz *.oxog_metrics.txt *.extra_info.json' % basename
    om.run_cmd(cmd)


if __name__ == "__main__":
    main()
