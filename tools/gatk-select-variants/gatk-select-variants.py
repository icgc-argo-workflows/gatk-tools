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
    parser.add_argument('-v', dest='input_vcf', type=str,
                        help='Input VCF', required=True)
    parser.add_argument('-i', dest='select_type_to_include', type=str,
                        help='Type of variant to include', required=True)
    parser.add_argument('-x', dest='select_type_to_exclude', type=str,
                        help='Type of variant to include', required=True)
    parser.add_argument('-o', dest='output_vcf_filename', type=str, required=True,
                        help='Output VCF filename')

    args = parser.parse_args()

    cmd = f"""
        gatk --java-options "-Xmx{args.jvm_mem}m" \
            SelectVariants \
            -V {args.input_vcf} \
            --create-output-variant-index \
            -O {args.output_vcf_filename} """

    if args.select_type_to_include:
        cmd = f"{cmd} --select-type-to-include {args.select_type_to_include} "

    elif args.select_type_to_exclude:
        cmd = f"{cmd} --select-type-to-exclude {args.select_type_to_exclude} "

    run_cmd(cmd)


if __name__ == "__main__":
    main()
