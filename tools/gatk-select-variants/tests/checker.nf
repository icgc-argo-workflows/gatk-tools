#!/usr/bin/env nextflow

/*
 * Copyright (c) 2019-2020, Ontario Institute for Cancer Research (OICR).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

/*
 * author Junjun Zhang <junjun.zhang@oicr.on.ca>
 */

nextflow.enable.dsl = 2

params.input_vcf = "NO_FILE"
params.select_type_to_include = ""
params.select_type_to_exclude = ""
params.output_basename = "my_variants"
params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB

include {gatkSelectVariants} from '../gatk-select-variants'

workflow {
  main:
    gatkSelectVariants(
      file(params.input_vcf),
      file(params.input_vcf + '.tbi'),
      params.select_type_to_include,
      params.select_type_to_exclude,
      params.output_basename
    )

}
