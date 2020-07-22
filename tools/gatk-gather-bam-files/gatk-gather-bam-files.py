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
    parser.add_argument('-i', dest='input_bams', type=str, nargs="+",
                        help='Input BAM files to be merged', required=True)
    parser.add_argument('-o', dest='output_bam_basename', type=str, required=True,
                        help='Name of the output merged BAM file')
    parser.add_argument('-c', dest='compression_level', type=int, default=5,
                        help='Compression level of the output BAM')

    args = parser.parse_args()

    input_bams = ' -I '.join(sorted(args.input_bams))  # this assumes the scatter files are named like: 0000-*, 0001-*, 00002-*

    cmd = f"""
        java -Dsamjdk.compression_level={args.compression_level} -Xms{args.jvm_mem}m -jar /gatk/gatk.jar \
            GatherBamFiles \
            -I {input_bams} \
            -O {args.output_bam_basename}.bam \
            --CREATE_INDEX true \
            --CREATE_MD5_FILE true """

    run_cmd(cmd)


if __name__ == "__main__":
    main()
