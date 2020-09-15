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
 *         Linda Xiang <linda.xiang@oicr.on.ca>
 */

nextflow.enable.dsl = 2

params.unfiltered_vcf = "NO_FILE"
params.ref_genome_fa = "NO_FILE"
params.contamination_table = "NO_FILE_cont"
params.segmentation_table = "NO_FILE_seg"
params.artifact_priors_tar_gz = "NO_FILE_ob"
params.mutect_stats = "NO_FILE_stats"
params.m2_extra_filtering_args = ""

params.cpus = 1
params.mem = 1  // in GB

include {gatkFilterMutectCalls; getSecondaryFiles} from '../gatk-filter-mutect-calls'

Channel
  .fromPath(getSecondaryFiles(params.unfiltered_vcf, ['tbi']), checkIfExists: true)
  .set { unfiltered_vcf_tbi_ch }

Channel
  .fromPath(getSecondaryFiles(params.ref_genome_fa, ['^dict', 'fai']), checkIfExists: true)
  .set { ref_genome_fai_ch }

artifact_priors_tar_gz = Channel.fromPath(params.artifact_priors_tar_gz)

workflow {
  main:
    gatkFilterMutectCalls(
      file(params.unfiltered_vcf),
      unfiltered_vcf_tbi_ch,
      file(params.ref_genome_fa),
      ref_genome_fai_ch.collect(),
      file(params.contamination_table),
      file(params.segmentation_table),
      artifact_priors_tar_gz.collect(),
      file(params.mutect_stats),
      params.m2_extra_filtering_args
    )
}

