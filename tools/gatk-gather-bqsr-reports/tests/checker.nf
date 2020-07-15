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

params.input_bqsr_reports = ["data/SA610149.0.20200122.wgs.grch38.cram.recal_data.csv"]
params.output_report_filename = 'recalibration-report.csv'
params.cpus = 1
params.mem = 1  // in GB

include gatkGatherBQSRReports from '../gatk-gather-bqsr-reports'

Channel
  .fromPath(params.input_bqsr_reports)
  .set { bqsr_reports }

workflow {
  main:
    gatkGatherBQSRReports(
      bqsr_reports,
      params.output_report_filename
    )

  publish:
    gatkGatherBQSRReports.out.bqsr_report to: "output"
}
