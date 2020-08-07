cwlVersion: v1.1
class: CommandLineTool
id: gatk-filter-mutect-calls

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-filter-mutect-calls:gatk-filter-mutect-calls.4.1.8.0-2.0'

baseCommand: [ 'gatk-filter-mutect-calls.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  unfiltered_vcf:
    type: File
    inputBinding:
      prefix: -V
    secondaryFiles: '.tbi'
  ref_fa:
    type: File
    inputBinding:
      prefix: -R
    secondaryFiles: ['.fai', '^.dict']
  contamination_table:
    type: File?
    inputBinding:
      prefix: --contamination-table
  segmentation_table:
    type: File?
    inputBinding:
      prefix: --tumor-segmentation
  artifact_priors_tar_gz:
    type: File[]?
    inputBinding:
      prefix: --ob-priors
  mutect_stats:
    type: File
    inputBinding:
      prefix: --stats
  m2_extra_filtering_args:
    type: string?
    inputBinding:
      prefix: -e

outputs:
  filtered_vcf:
    type: File
    outputBinding:
      glob: "*.filtered.vcf.gz"
    secondaryFiles: '.tbi'
  filtering_stats:
    type: File
    outputBinding:
      glob: "*.filtering-stats"
