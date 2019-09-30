#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK GetPileupSummaries')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-R', dest='ref_fa', type=str,
                        help='Reference genome file (eg, .fa)')
    parser.add_argument('-I', dest='input_seq', type=str,
                        help='BAM/SAM/CRAM file containing reads', required=True)
    parser.add_argument('-L', dest='intervals', type=str,
                        help='One or more genomic intervals over which to operate', required=True)
    parser.add_argument('-V', dest='variants', type=str,
                        help='A VCF file containing variants and allele frequencies', required=True)
    parser.add_argument('-O', dest='output_name', type=str,
                        help='Output file name', required=True)

    args = parser.parse_args()

    cmd = 'gatk --java-options "-Xmx%sm" GetPileupSummaries -I %s -L %s -V %s -O %s --interval-set-rule INTERSECTION' % (
            args.jvm_mem, args.input_seq, args.intervals, args.variants, args.output_name
        )

    if args.ref_fa:
        cmd = cmd + ' -R %s' % args.ref_fa

    try:
        p = subprocess.run([cmd],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        print(p.stdout.decode("utf-8"))
        print(p.stderr.decode("utf-8"), file=sys.stderr)

        if p.returncode != 0:
            sys.exit(p.returncode if p.returncode else 1)

    except Exception as e:
        sys.exit('Execution failed: %s' % e)


if __name__ == "__main__":
    main()
