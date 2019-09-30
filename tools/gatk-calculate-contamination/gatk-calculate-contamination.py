#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK CalculateContamination')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-I', dest='tumour_pileups', type=str,
                        help='Pileup summary from tumour reads', required=True)
    parser.add_argument('-matched', dest='normal_pileups', type=str,
                        help='Pileup summary from matched normal reads')
    parser.add_argument('--tumor-segmentation', dest='segmentation_output', type=str,
                        help='Output file name for tumour segment table')
    parser.add_argument('-O', dest='contamination_output', type=str,
                        help='Output file name for contamination table', required=True)

    args = parser.parse_args()

    cmd = 'gatk --java-options "-Xmx%sm" CalculateContamination -I %s --tumor-segmentation %s -O %s' % (
            args.jvm_mem, args.tumour_pileups, args.segmentation_output, args.contamination_output
        )

    if args.normal_pileups:
        cmd = cmd + ' -matched %s' % args.normal_pileups

    try:
        p = subprocess.run([cmd],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        print(p.stdout.decode("utf-8"))
        if p.returncode != 0:
            print('Error occurred: %s' % p.stderr.decode("utf-8"), file=sys.stderr)
            sys.exit(p.returncode)

    except Exception as e:
        sys.exit('Execution failed: %s' % e)


if __name__ == "__main__":
    main()
