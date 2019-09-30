#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK FilterAlignmentArtifacts')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('--bwa-mem-index-image', dest='bwa_mem_index_image', type=str,
                        help='Pileup summary from matched normal reads', required=True)
    parser.add_argument('-I', dest='tumour_seq', type=str,
                        help='BAM/SAM/CRAM file containing tumour reads', required=True)
    parser.add_argument('-V', dest='input_vcf', type=str,
                        help='A VCF file containing variants', required=True)
    parser.add_argument('-O', dest='output_vcf', type=str,
                        help='The output filtered VCF file', required=True)

    args = parser.parse_args()

    cmd = 'gatk --java-options "-Xmx%sm" FilterAlignmentArtifacts --bwa-mem-index-image %s -I %s -V %s -O %s' % (
            args.jvm_mem, args.bwa_mem_index_image, args.tumour_seq, args.input_vcf, args.output_vcf
        )

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
