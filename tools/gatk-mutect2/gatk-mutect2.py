#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

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
    parser.add_argument('-p', '--panel-of-normals', dest='panel_of_normals', type=str,
                        help='VCF file of sites observed in normal.')                    
    parser.add_argument('-L', '--intervals', dest='intervals', type=str,
                        help='One or more genomic intervals over which to operate')
    parser.add_argument('-O', '--output-vcf', dest='output_vcf', type=str,
                        help='Output file with only the sample name in it.', required=True)
    parser.add_argument('-b', '--bam-output', dest='bam_output', type=str,
                        help='File to which assembled haplotypes should be written')
    parser.add_argument('-f', '--f1r2-tar-gz', dest='f1r2_tar_gz', type=str,
                        help='collect F1R2 counts and output files into this tar.gz file')

    args = parser.parse_args()

    output_prefix = ''
    if args.intervals:
        output_prefix = os.path.basename(args.intervals).split('.')[0] + '.'

    if not args.output_vcf.endswith('.vcf.gz'):
        sys.exit('Usage: output VCF file name must end with ".vcf.gz"')

    if args.bam_output and not args.bam_output.endswith('.bam'):
        sys.exit('Usage: BAM output file name must end with ".bam"')

    if args.f1r2_tar_gz and not args.f1r2_tar_gz.endswith('.tar.gz'):
        sys.exit('Usage: f1r2_tar_gz output file name must end with ".tar.gz"')

    cmd = 'gatk --java-options "-Xmx%sm" Mutect2 -R %s -O %s%s -I %s' % (
            args.jvm_mem, args.ref_fa, output_prefix, args.output_vcf, args.tumour_reads
        )

    if args.germline_resource:
        cmd = cmd + ' --germline-resource %s' % args.germline_resource

    if args.panel_of_normals:
        cmd = cmd + ' --panel-of-normals %s' % args.panel_of_normals
        cmd = cmd + ' --genotype-pon-sites'

    if args.normal_reads:
        p = subprocess.run(['samtools view -H %s | grep "^@RG" | tr \'\t\' \'\n\' | grep "^SM" | sort -u' % args.normal_reads],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        if p.returncode == 0:
            normal_sample_name = p.stdout.decode('ascii').rstrip()
            if normal_sample_name.count('\n'):
                sys.exit('Normal reads file has more than one SM value in the header, only one SM is allowed.')
            else:
                normal_cmd = ' -I %s -normal %s' % (args.normal_reads, normal_sample_name.replace('SM:', '', 1))
                cmd = cmd + normal_cmd
        else:
            sys.exit('Unable to get "SM" from normal reads file. Error: %s' % p.stderr)

    if args.intervals:
        cmd = cmd + ' -L %s' % args.intervals

    if args.bam_output:
        cmd = cmd + ' --bam-output %s%s' % (output_prefix, args.bam_output)

    if args.f1r2_tar_gz:
        cmd = cmd + ' --f1r2-tar-gz %s%s' % (output_prefix, args.f1r2_tar_gz)

    run_cmd(cmd)


if __name__ == "__main__":
    main()
