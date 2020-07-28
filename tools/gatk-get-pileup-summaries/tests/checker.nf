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

params.seq = "data/HCC1143_BL-mini-N/cfa409d0-3236-5f07-8634-a2c0de74c8f2.5.20190927.wgs.grch38.bam"
params.ref_genome_fa = "reference/tiny-grch38-chr11-530001-537000.fa"
params.variants_resources = "data/tiny-chr11-exac_common_3.hg38.vcf.gz"
params.interval_file = "NO_FILE"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB


include {gatkGetPileupSummaries; getSecondaryFiles} from '../gatk-get-pileup-summaries'

Channel
  .fromPath(getSecondaryFiles(params.seq, ['bai', 'crai']))
  .set { seq_sec_ch }

Channel
  .fromPath(getSecondaryFiles(params.ref_genome_fa, ['fai', '^dict']), checkIfExists: true)
  .set { ref_genome_sec_ch }

Channel
  .fromPath(getSecondaryFiles(params.variants_resources, ['tbi']), checkIfExists: true)
  .set { variants_sec_ch }

workflow {
  main:
    gatkGetPileupSummaries(
      file(params.seq),
      seq_sec_ch.collect(),
      file(params.ref_genome_fa),
      ref_genome_sec_ch.collect(),
      file(params.variants_resources),
      variants_sec_ch.collect(),
      file(params.interval_file)
    )

}
