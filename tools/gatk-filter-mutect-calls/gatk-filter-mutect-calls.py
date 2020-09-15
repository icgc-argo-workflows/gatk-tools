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
    parser.add_argument('--stats', dest='mutect_stats', type=str,
                        help='The Mutect stats file output by Mutect2', required=True)
    parser.add_argument('-e', dest='m2_extra_filtering_args', type=str,
                        help='The Mutect2 extra filtering parameters')

    args = parser.parse_args()

    basename = re.sub(r'\.vcf\.gz$', '', os.path.basename(args.unfiltered_vcf))

    cmd = 'gatk --java-options "-Xmx%sm" FilterMutectCalls -V %s -R %s -O %s --filtering-stats %s --stats %s' % (
            args.jvm_mem, args.unfiltered_vcf, args.ref_fa, basename+'.filtered.vcf.gz', 'filter-mutect-calls.filtering-stats', args.mutect_stats
        )

    if args.contamination_table:
        cmd = cmd + ' --contamination-table %s' % args.contamination_table
    if args.segmentation_table:
        cmd = cmd + ' --tumor-segmentation %s' % args.segmentation_table
    if args.artifact_priors_tar_gz:
        for p in args.artifact_priors_tar_gz:
            cmd = cmd + ' -ob-priors %s' % p
    if args.m2_extra_filtering_args:
        cmd = cmd + ' %s' % args.m2_extra_filtering_args

    run_cmd(cmd)


if __name__ == "__main__":
    main()
