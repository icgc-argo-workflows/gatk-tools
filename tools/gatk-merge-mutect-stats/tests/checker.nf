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

nextflow.preview.dsl = 2

params.input_stats = "data/HCC1143-mini-Mutect2-calls/HCC1143.mutect2.vcf.gz.stats"
params.output_basename = "merged"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB

include gatkMergeMutectStats from '../gatk-merge-mutect-stats'

workflow {
  main:
    gatkMergeMutectStats(
      file(params.input_stats),
      params.output_basename
    )
}
