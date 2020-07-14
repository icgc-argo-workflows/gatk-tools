#!/usr/bin/env python3

"""
Copyright (c) 2019-2020, Ontario Institute for Cancer Research (OICR).
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
Authors:
  Junjun Zhang <junjun.zhang@oicr.on.ca>
"""


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
    parser = argparse.ArgumentParser(description='GATK BaseRecalibrator')

    parser.add_argument('-m', '--jvm-mem', dest='jvm_mem', type=int,
                        help='JVM max memory in MB', default=500)
    parser.add_argument('-s', dest='input_bam', type=str,
                        help='Input BAM/CRAM', required=True)
    parser.add_argument('-r', dest='reference', type=str,
                        help='Reference genome sequence fa file', required=True)
    parser.add_argument('-c', dest='recalibration_report', type=str, required=True,
                        help='Recalibration report file')
    parser.add_argument('-o', dest='output_bam_basename', type=str, required=True,
                        help='Basename of the output recalibrated BAM')
    parser.add_argument('-k', dest='compression_level', type=int,
                        help='Compression level of output BAM', default=5)
    parser.add_argument('-i', dest='interval_file', type=str,
                        help='Interval file, eg, bed file, to specify working interval')

    args = parser.parse_args()

    cmd = f"""
        gatk --java-options "-XX:+PrintFlagsFinal -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps \
            -XX:+PrintGCDetails -Xloggc:gc_log.log -XX:GCTimeLimit=50 -XX:GCHeapFreeLimit=10 \
            -Dsamjdk.compression_level={args.compression_level} -Xms{args.jvm_mem}m" \
            ApplyBQSR \
            --create-output-bam-md5 \
            --add-output-sam-program-record \
            -R {args.reference} \
            -I {args.input_bam} \
            --use-original-qualities \
            -bqsr {args.recalibration_report} \
            --static-quantized-quals 10 \
            --static-quantized-quals 20 \
            --static-quantized-quals 30 \
            -O {args.output_bam_basename}.bam """

    if args.interval_file:
        cmd = f"{cmd} -L {args.interval_file}"

    run_cmd(cmd)


if __name__ == "__main__":
    main()
