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
        print('Execution returned non-zero code: %s. Additional error message: %s' % \
                (e.returncode, e.stderr.decode("utf-8")), file=sys.stderr)
        sys.exit(e.returncode)

    except Exception as e:  # all other errors go here, like unable to find the command
        sys.exit('Execution failed: %s' % e)

    return p  # in case the caller of this funtion needs p.stdout, p.stderr etc


def main():
    parser = argparse.ArgumentParser(description='GATK CollectOxoGMetrics')

    parser.add_argument('-m', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-s', dest='seq', type=str,
                        help='Input BAM/CRAM', required=True)
    parser.add_argument('-r', dest='reference', type=str,
                        help='Reference genome sequence fa file', required=True)


    args = parser.parse_args()

    metrics_file = "%s.oxog_metrics.txt" % args.seq
    jvm_Xmx = "-Xmx%sm" % args.jvm_mem
    
    # detect the format of input file
    if os.path.basename(args.seq).endswith(".bam"):
        cmd = f'gatk --java-options {jvm_Xmx} CollectOxoGMetrics -I {args.seq} -O {metrics_file} -R {args.reference}'

    elif os.path.basename(args.seq).endswith(".cram"):
        cmd = (
            f'samtools view -b -T {args.reference} {args.seq} -o /dev/stdout | '
            f'gatk --java-options {jvm_Xmx} CollectOxoGMetrics -I /dev/stdin -O {metrics_file} -R {args.reference}')

    else:
        sys.exit("Unsupported input file format!")

    run_cmd(cmd)

    cmd = 'tar czf %s.oxog_metrics.tgz *.oxog_metrics.txt' % args.seq
    run_cmd(cmd)


if __name__ == "__main__":
    main()
