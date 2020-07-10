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
version = '4.1.8.0-1.0'

params.seq = "NO_FILE"
params.interval_file = "NO_FILE"
params.container_version = ""
params.ref_genome_fa = "NO_FILE"
params.known_snv_indel_sites_vcfs = []
params.cpus = 1
params.mem = 1  // in GB


def getSecondaryFiles(main_file, exts){
    def secondaryFiles = []
    for (ext in exts) {
        secondaryFiles.add(main_file + '.' + ext)
    }
    return secondaryFiles
}


process gatkBaseRecalibrator {
  container "quay.io/icgc-argo/gatk-base-recalibrator:gatk-base-recalibrator.${params.container_version ?: version}"
  cpus params.cpus
  memory "${params.mem} GB"

  input:
    path seq
    path seq_idx
    path ref_genome_fa
    path ref_genome_secondary_file
    path known_snv_indel_sites_vcfs
    path interval_file

  output:
    path "*.recal_data.csv", emit: recalibration_report

  script:
    arg_interval_file = interval_file.name == 'NO_FILE' ? "" : "-i ${interval_file}"
    arg_known_sites = known_snv_indel_sites_vcfs.count() == 0 ? "" : "-k ${known_snv_indel_sites_vcfs}"

    """
    gatk-base-recalibrator.py -s ${seq} \
                      -r ${ref_genome_fa} \
                      -m ${(int) (params.mem * 1000)} \
                      -o ${seq}.recal_data.csv ${arg_interval_file} ${arg_known_sites}
    """
}


Channel
  .fromPath(getSecondaryFiles(params.seq, ['crai']), checkIfExists: true)
  .set { seq_crai_ch }

Channel
  .fromPath(getSecondaryFiles(params.ref_genome_fa, ['fai']), checkIfExists: true)
  .set { ref_genome_fai_ch }

if (params.known_snv_indel_sites_vcfs) {
  known_sites = Channel.fromPath(params.known_snv_indel_sites_vcfs)
} else {
  known_sites = Channel.empty()
}

workflow {
  main:
    gatkBaseRecalibrator(
      file(params.seq),
      seq_crai_ch,
      file(params.ref_genome_fa),
      ref_genome_fai_ch,
      known_sites,
      file(params.interval_file)
    )

  publish:
    gatkBaseRecalibrator.out.recalibration_report to: "output"
}
