#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK GatherPileupSummaries')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-D', dest='ref_dict', type=str,
                        help='Reference sequence .dict file', required=True)
    parser.add_argument('-I', dest='input_pileup', type=str,
                        help='Input pipeup summary table file(s)', nargs="+", required=True)
    parser.add_argument('-O', dest='output_name', type=str,
                        help='Output file name', required=True)

    args = parser.parse_args()

    if not args.output_name.endswith('.tsv'):
        sys.exit('Usage: -O output file name must end with ".tsv"')

    cmd = 'gatk --java-options "-Xmx%sm" GatherPileupSummaries --sequence-dictionary %s -O %s' % (
            args.jvm_mem, args.ref_dict, args.output_name
        )

    for i in args.input_pileup:
        cmd = cmd + ' -I %s' % i

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
