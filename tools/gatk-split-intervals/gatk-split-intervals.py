#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK SplitIntervals')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-R', dest='ref_fa', type=str,
                        help='Reference genome file (eg, .fa)', required=True)
    parser.add_argument('-L', dest='intervals', type=str,
                        help='Optional interval file with one or more genomic intervals over which to operate')
    parser.add_argument('--scatter', dest='scatter_count', type=int,
                        help='Number of output interval files to split into', required=True)

    args = parser.parse_args()

    cmd = 'gatk --java-options "-Xmx%sm" SplitIntervals -R %s -O %s -scatter %s' % (
            args.jvm_mem, args.ref_fa, os.getcwd(), args.scatter_count
        )

    if args.intervals:
        cmd = cmd + ' -L %s' % args.intervals

    p, success = None, True
    try:
        p = subprocess.run([cmd],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        print(p.stdout.decode("utf-8"))
        print(p.stderr.decode("utf-8"), file=sys.stderr)

    except Exception as e:
        print('Execution failed: %s' % e, file=sys.stderr)
        success = False

    if p and p.returncode != 0:
        success = False

    if not success:
        sys.exit(p.returncode if p.returncode else 1)


if __name__ == "__main__":
    main()
