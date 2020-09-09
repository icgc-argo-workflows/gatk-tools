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

nextflow.enable.dsl = 2
version = '4.1.8.0-3.0'

params.seq_pileups = "NO_FILE"
params.matched_pileups = "NO_FILE"

params.container_version = ""
params.cpus = 1
params.mem = 1  // in GB


process gatkCalculateContamination {
  container "quay.io/icgc-argo/gatk-calculate-contamination:gatk-calculate-contamination.${params.container_version ?: version}"
  cpus params.cpus
  memory "${params.mem} GB"
  //publishDir "output/calculateContamination"

  input:
    path seq_pileups
    path matched_pileups

  output:
    path "*.contamination_metrics", emit: contamination_metrics
    path "*.segmentation_metrics", emit: segmentation_metrics

  script:

    arg_matched_pileups = matched_pileups.name == 'NO_FILE' ? "" : "-matched ${matched_pileups}"

    """
    gatk-calculate-contamination.py -I ${seq_pileups} \
                      ${arg_matched_pileups} \
                      -j ${(int) (params.mem * 1000)} 
    """
}
