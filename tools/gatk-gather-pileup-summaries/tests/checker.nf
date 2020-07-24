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
 *        Linda Xiang  <linda.xiang@oicr.on.ca>
 */

nextflow.preview.dsl = 2

params.ref_genome_dict = "reference/tiny-grch38-chr11-530001-537000.dict"
params.input_pileup = "NO_FILE"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB


include gatkGatherPileupSummaries from '../gatk-gather-pileup-summaries'

Channel
  .fromPath(params.input_pileup, checkIfExists: true)
  .set { input_pileup_ch }

workflow {
  main:
    gatkGatherPileupSummaries(
      file(params.ref_genome_dict),
      input_pileup_ch.collect()
    )

  publish:
    gatkGatherPileupSummaries.out.merged_pileups_metrics to: "output"
}
