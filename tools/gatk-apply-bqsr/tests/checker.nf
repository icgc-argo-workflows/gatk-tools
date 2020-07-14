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

params.seq = "data/SA610149.0.20200122.wgs.grch38.cram"
params.interval_file = "NO_FILE"
params.ref_genome_fa = "reference/tiny-grch38-chr11-530001-537000.fa"
params.recalibration_report = "NO_FILE"
params.cpus = 1
params.mem = 1  // in GB

include {gatkApplyBQSR; getSecondaryFiles} from '../gatk-apply-bqsr'

Channel
  .fromPath(getSecondaryFiles(params.seq, ['crai']), checkIfExists: true)
  .set { seq_crai_ch }

Channel
  .fromPath(getSecondaryFiles(params.ref_genome_fa, ['^dict', 'fai']), checkIfExists: true)
  .set { ref_genome_fai_ch }

known_sites_vcfs = Channel.fromPath(params.known_sites_vcfs)

known_sites_indices = known_sites_vcfs.flatMap { v -> getSecondaryFiles(v, ['tbi']) }

workflow {
  main:
    gatkBaseRecalibrator(
      file(params.seq),
      seq_crai_ch,
      file(params.ref_genome_fa),
      ref_genome_fai_ch.collect(),
      known_sites_vcfs.collect(),
      known_sites_indices.collect(),
      file(params.interval_file)
    )

  publish:
    gatkBaseRecalibrator.out.recalibration_report to: "output"
}
