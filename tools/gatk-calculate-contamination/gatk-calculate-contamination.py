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
    parser = argparse.ArgumentParser(description='GATK CalculateContamination')

    parser.add_argument('-j', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=1000)
    parser.add_argument('-I', dest='seq_pileups', type=str,
                        help='Pileup summary from seq reads', required=True)
    parser.add_argument('-matched', dest='matched_pileups', type=str,
                        help='Pileup summary from matched normal reads')

    args = parser.parse_args()

    basename = re.sub(r'\.pileups_metrics\.tsv$', '', os.path.basename(args.seq_pileups))
    if args.matched_pileups:
        basename = basename + '.tumour'
    else:
        basename = basename + '.normal' 
    
    cmd = 'gatk --java-options "-Xmx%sm" CalculateContamination -I %s -O %s.contamination_metrics \
                -segments %s.segmentation_metrics' % (
            args.jvm_mem, args.seq_pileups, basename, basename
        )

    if args.matched_pileups:
        cmd = cmd + ' -matched %s' % args.matched_pileups

    run_cmd(cmd)


if __name__ == "__main__":
    main()
