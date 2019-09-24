#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='GATK Mutect2')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-R', dest='ref_fa', type=str,
                        help='Reference genome file (eg, .fa)', required=True)
    parser.add_argument('-t', '--tumour-reads', dest='tumour_reads', type=str,
                        help='Tumour reads file, bam or cram', required=True)
    parser.add_argument('-n', '--normal-reads', dest='normal_reads', type=str,
                        help='Normal reads file, bam or cram')
    parser.add_argument('-g', '--germline-resource', dest='germline_resource', type=str,
                        help='Population VCF of germline sequencing containing allele fractions, af-only-gnomad.vcf.gz.')
    parser.add_argument('-L', '--intervals', dest='intervals', type=str,
                        help='One or more genomic intervals over which to operate')
    parser.add_argument('-O', '--output-vcf', dest='output_vcf', type=str,
                        help='Output file with only the sample name in it.', required=True)
    parser.add_argument('-b', '--bam-output', dest='bam_output', type=str,
                        help='File to which assembled haplotypes should be written')
    parser.add_argument('-f', '--f1r2-tar-gz', dest='f1r2_tar_gz', type=str,
                        help='collect F1R2 counts and output files into this tar.gz file')

    args = parser.parse_args()

    # TODO: valid arguments, output_vcf must end with 'vcf.gz', bam_output must end with '.bam'
    # f1r2_tar_gz must end with '.tar.gz'

    # TODO: get normal sample name, use it as -normal when invoke Mutect2
    normal_cmd = ''
    if normal_reads:
        normal_sample_name = 'test-normal'
        normal_cmd = '-I %s -normal %s' % (normal_reads, normal_sample_name)

    cmd = 'gatk --java-options "-Xmx%sm" Mutect2 -R %s -O %s -I %s %s' % (
            jvm_mem, ref_fa, output_vcf, tumour_reads, normal_cmd
        )

    if intervals:
        cmd = cmd + ' -L %s' % intervals

    if bam_output:
        cmd = cmd + ' --bam-output %s' % bam_output

    if f1r2_tar_gz:
        cmd = cmd + ' --f1r2-tar-gz %s' % f1r2_tar_gz

    stdout, stderr, p, success = '', '', None, True
    try:
        p = subprocess.Popen([cmd],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        stdout, stderr = p.communicate()

    except Exception as e:
        print('Execution failed: %s' % e, file=sys.stderr)
        success = False

    if p and p.returncode != 0:
        print('Execution failed, none zero code returned. Error: %s' % stderr.decode("utf-8"),
            file=sys.stderr)
        success = False

    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"), file=sys.stderr)

    if not success:
        sys.exit(p.returncode if p.returncode else 1)

if __name__ == "__main__":
    main()
