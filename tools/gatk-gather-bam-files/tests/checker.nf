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

params.input_bams = "NO_FILE"
params.output_bam_basename = "final_bam"
params.compression_level = "null"

params.cpus = 1
params.mem = 1  // in GB

include gatkGatherBamFiles from '../gatk-gather-bam-files'

Channel
  .fromPath(params.input_bams)
  .set { input_bams }

workflow {
  main:
    gatkGatherBamFiles(
      input_bams.collect(),
      params.output_bam_basename,
      params.compression_level
    )

  publish:
    gatkGatherBamFiles.out.merged_bam to: "output"
}
