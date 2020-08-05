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
version = '4.1.8.0-2.0'

params.seq = "NO_FILE"
params.interval_file = "NO_FILE"
params.container_version = ""
params.ref_genome_fa = "NO_FILE"
params.known_sites_vcfs = "NO_FILE"
params.cpus = 1
params.mem = 1  // in GB


process gatkFilterAlignmentArtifacts {
  container "quay.io/icgc-argo/gatk-filter-alignment-artifacts:gatk-filter-alignment-artifacts.${params.container_version ?: version}"
  cpus params.cpus
  memory "${params.mem} GB"

  input:
    path tumour_seq
    path tumour_seq_idx
    path bwa_mem_index_image
    path input_vcf
    path input_vcf_idx
    val output_vcf_basename

  output:
    path "${output_vcf_basename}.vcf.gz", emit: filtered_vcf
    path "${output_vcf_basename}.vcf.gz.tbi", emit: filtered_vcf_idx

  script:
    """
    gatk-filter-alignment-artifacts.py \
                      -j ${(int) (params.mem * 1000)} \
                      -I ${tumour_seq} \
                      -V ${input_vcf} \
                      --bwa-mem-index-image ${bwa_mem_index_image} \
                      -O ${output_vcf_basename}.vcf.gz
    """
}
