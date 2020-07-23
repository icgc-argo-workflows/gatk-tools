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

params.tumour_reads = "data/HCC1143-mini-T/8f879c15-14da-593d-bb76-db866f81ab3a.6.20190927.wgs.grch38.bam"
params.normal_reads = "data/HCC1143_BL-mini-N/cfa409d0-3236-5f07-8634-a2c0de74c8f2.5.20190927.wgs.grch38.bam"
params.interval_file = "data/0000-scattered.interval_list"
params.ref_genome_fa = "reference/tiny-grch38-chr11-530001-537000.fa"
params.germline_resource = "data/*.vcf.gz"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB

include {gatkMutect2; getSecondaryFiles} from '../gatk-mutect2'

Channel
  .fromPath(getSecondaryFiles(params.tumour_reads, ['bai']), checkIfExists: true)
  .set { tumour_idx_ch }

Channel
  .fromPath(getSecondaryFiles(params.normal_reads, ['bai']), checkIfExists: true)
  .set { normal_idx_ch }

Channel
  .fromPath(getSecondaryFiles(params.ref_genome_fa, ['^dict', 'fai']), checkIfExists: true)
  .set { ref_genome_secondary_file }

germline_resource = Channel.fromPath(params.germline_resource)

germline_resource_idx = germline_resource.flatMap { v -> getSecondaryFiles(v, ['tbi']) }

workflow {
  main:
    gatkMutect2(
      file(params.tumour_reads),
      tumour_idx_ch,
      file(params.normal_reads),
      normal_idx_ch,
      file(params.ref_genome_fa),
      ref_genome_secondary_file,
      germline_resource,
      germline_resource_idx,
      file(params.interval_file)
    )

  publish:
    gatkMutect2.out.output_vcf to: "output"
    gatkMutect2.out.mutect_stats to: "output"
    gatkMutect2.out.bam_output to: "output"
    gatkMutect2.out.f1r2_counts to: "output"
}
