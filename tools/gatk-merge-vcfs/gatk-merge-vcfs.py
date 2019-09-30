#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK MergeVcfs')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-I', dest='input_vcf', type=str,
                        help='Input VCF file(s)', nargs="+", required=True)
    parser.add_argument('-O', dest='output_name', type=str,
                        help='Output file name', required=True)

    args = parser.parse_args()

    if not args.output_name.endswith('.vcf.gz'):
        sys.exit('Usage: -O output file name must end with ".vcf.gz"')

    cmd = 'gatk --java-options "-Xmx%sm" MergeVcfs -O %s' % (
            args.jvm_mem, args.output_name
        )

    for i in args.input_vcf:
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
