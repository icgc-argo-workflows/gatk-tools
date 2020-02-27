#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import csv
import re
import json
from math import log10

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

def get_oxoQ(oxog_metric):
    num = 0
    NTOT = 0
    NALTOXO = 0
    NALTNON = 0
    oxoQ = float('NaN')
    with open(oxog_metric, 'r') as fp:
        oxoReader = csv.DictReader(filter(lambda row: not re.match(r'^#|\s*$', row), fp), delimiter='\t')

        for line in oxoReader:
            CTXT = line['CONTEXT']
            if re.match('CCG', CTXT):
                num = num + 1
                NTOT = NTOT + int(line['TOTAL_BASES'])
                NALTOXO = NALTOXO + int(line['ALT_OXO_BASES'])
                NALTNON = NALTNON + int(line['ALT_NONOXO_BASES'])
                oxoQ = float(line['OXIDATION_Q'])

    if num > 1:
        er = float(max(NALTOXO - NALTNON, 1.0001)) / float(NTOT)
        oxoQ = -10.0 * log10(er)

    return oxoQ


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

    version_cmd = 'gatk CollectOxoGMetrics --version | grep GATK'
    p = run_cmd(version_cmd)
    tool_ver = 'gatk:CollectOxoGMetrics@%s' % p.stdout.decode("utf-8").strip().split(' ')[-1]

    oxoQ_score = get_oxoQ(metrics_file)
    with open("%s.extra_info.json" % args.seq, 'w') as f:
        f.write(json.dumps({
                "tool": tool_ver,
                "oxoQ_score": float('%.4f' % oxoQ_score),
                "context": "CCG"
            }, indent=2))

    cmd = 'tar czf %s.oxog_metrics.tgz %s.oxog_metrics.txt *.extra_info.json' % (args.seq, args.seq)
    run_cmd(cmd)


if __name__ == "__main__":
    main()
