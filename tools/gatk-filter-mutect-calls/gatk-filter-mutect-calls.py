#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK FilterMutectCalls')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-V', dest='unfiltered_vcf', type=str,
                        help='Unfiltered VCF file', required=True)
    parser.add_argument('-R', dest='ref_fa', type=str,
                        help='Reference sequence', required=True)
    parser.add_argument('--contamination-table', dest='contamination_table', type=str,
                        help='Contamination table file')
    parser.add_argument('--tumor-segmentation', dest='segmentation_table', type=str,
                        help='Tumour segmentation table file')
    parser.add_argument('--ob-priors', dest='artifact_priors_tar_gz', nargs='+', type=str,
                        help='One or more .tar.gz files containing tables of prior artifact probabilities for the read orientation filter model, one table per tumor sample')
    parser.add_argument('--stats', dest='metect_stats', type=str,
                        help='The Mutect stats file output by Mutect2', required=True)
    parser.add_argument('--filtering-stats', dest='filtering_stats_output', type=str,
                        help='The output filtering stats file')
    parser.add_argument('-O', dest='output_vcf', type=str,
                        help='Output file name for filtered VCF', required=True)

    args = parser.parse_args()

    cmd = 'gatk --java-options "-Xmx%sm" FilterMutectCalls -V %s -R %s -O %s --stats %s' % (
            args.jvm_mem, args.unfiltered_vcf, args.ref_fa, args.output_vcf, args.metect_stats
        )

    if args.contamination_table:
        cmd = cmd + ' --contamination-table %s' % args.contamination_table
    if args.segmentation_table:
        cmd = cmd + ' --tumor-segmentation %s' % args.segmentation_table
    if args.artifact_priors_tar_gz:
        for p in args.artifact_priors_tar_gz:
            cmd = cmd + ' -ob-priors %s' % p
    if args.filtering_stats_output:
        cmd = cmd + ' --filtering-stats %s' % args.filtering_stats_output

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
