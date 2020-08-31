#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import re
import hashlib


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
    parser = argparse.ArgumentParser(description='GATK GatherPileupSummaries')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-D', dest='ref_dict', type=str,
                        help='Reference sequence .dict file', required=True)
    parser.add_argument('-I', dest='input_pileup', type=str,
                        help='Input pipeup summary table file(s)', nargs="+", required=True)
    

    args = parser.parse_args()

    basename = hashlib.md5('\t'.join(args.input_pileup))

    cmd = 'gatk --java-options "-Xmx%sm" GatherPileupSummaries --sequence-dictionary %s -O %s.pileups_metrics.tsv' % (
            args.jvm_mem, args.ref_dict, basename
        )

    for i in args.input_pileup:
        cmd = cmd + ' -I %s' % i

    run_cmd(cmd)


if __name__ == "__main__":
    main()
