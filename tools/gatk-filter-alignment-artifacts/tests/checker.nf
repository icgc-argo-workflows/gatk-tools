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


params.tumour_seq = "data/HCC1143-mini-T/8f879c15-14da-593d-bb76-db866f81ab3a.6.20190927.wgs.grch38.bam"
params.bwa_mem_index_image = "reference/tiny-grch38-chr11-530001-537000.fa.img"
params.input_vcf = "data/HCC1143-mini-Mutect2-calls/HCC1143.mutect2.vcf.gz"
params.output_vcf_basename = "aa_filtered_vcf"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB

include gatkFilterAlignmentArtifacts from '../gatk-filter-alignment-artifacts'


def getSecondaryFiles(main_file, exts){
  def secondaryFiles = []
  for (ext in exts) {
    if (ext.startsWith("^")) {
      ext = ext.replace("^", "")
      parts = main_file.split("\\.").toList()
      parts.removeLast()
      secondaryFiles.add((parts + [ext]).join("."))
    } else {
      secondaryFiles.add(main_file + '.' + ext)
    }
  }
  return secondaryFiles
}


workflow {
  main:
    gatkFilterAlignmentArtifacts(
      file(params.tumour_seq),
      Channel.fromPath(getSecondaryFiles(params.tumour_seq, ['bai', 'crai'])),
      file(params.bwa_mem_index_image),
      file(params.input_vcf),
      Channel.fromPath(getSecondaryFiles(params.input_vcf, ['tbi']), checkIfExists: true),
      params.output_vcf_basename
    )
}
