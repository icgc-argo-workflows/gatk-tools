#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import re

def run_cmd(cmd):
    try:
        p = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           shell=True, check=True)

    except subprocess.CalledProcessError as e:   # this is triggered when cmd returned non-zero code
        print(e.stdout.decode("utf-8"))
        print('Execution returned non-zero code: %s. Additional error message: %s' %
              (e.returncode, e.stderr.decode("utf-8")), file=sys.stderr)
        sys.exit(e.returncode)

    except Exception as e:  # all other errors go here, like unable to find the command
        sys.exit('Execution failed: %s' % e)

    return p  # in case the caller of this funtion needs p.stdout, p.stderr etc

def main():
    parser = argparse.ArgumentParser(description='GATK CalculateContamination')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-I', dest='tumour_pileups', type=str,
                        help='Pileup summary from tumour reads', required=True)
    parser.add_argument('-matched', dest='normal_pileups', type=str,
                        help='Pileup summary from matched normal reads')
    parser.add_argument('-s', dest='specimen_type', type=str,
                        help='Specify whether it is normal or tumour and allow output files name contain the speciment info')

    args = parser.parse_args()

    basename = re.sub(r'\.pileups_metrics\.tsv$', '', os.path.basename(args.tumour_pileups))
    if args.specimen_type:
        basename = basename + '.' + args.specimen_type
    
    cmd = 'gatk --java-options "-Xmx%sm" CalculateContamination -I %s -O %s.contamination_metrics \
                --tumor-segmentation %s.segmentation_metrics' % (
            args.jvm_mem, args.tumour_pileups, basename, basename
        )

    if args.normal_pileups:
        cmd = cmd + ' -matched %s' % args.normal_pileups

    run_cmd(cmd)


if __name__ == "__main__":
    main()
