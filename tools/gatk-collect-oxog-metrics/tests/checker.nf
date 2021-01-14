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
 *        Linda Xiang <linda.xiang@oicr.on.ca>
 */

nextflow.enable.dsl=2

params.seq = ""
params.seq_idx = ""
params.ref_genome_fa = ""
params.interval_file = "NO_FILE"
params.paired = true
params.analysis_metadata = "NO_FILE"

include { gatkCollectOxogMetrics; getOxogSecondaryFiles; getPairedEndFlag; gatherOxogMetrics } \
  from '../gatk-collect-oxog-metrics.nf' params(params)

Channel
  .fromPath(getOxogSecondaryFiles(params.ref_genome_fa), checkIfExists: true)
  .set { ref_genome_ch }


workflow {
  main:
    def paired = params.paired
    if (params.analysis_metadata != "NO_FILE") {
      paired = getPairedEndFlag(params.analysis_metadata)
    }

    gatkCollectOxogMetrics(
      file(params.seq),
      file(params.seq_idx),
      file(params.ref_genome_fa),
      ref_genome_ch.collect(),
      file(params.interval_file),
      paired,
      true
    )

    gatherOxogMetrics(
      gatkCollectOxogMetrics.out.oxog_metrics
    )
}
