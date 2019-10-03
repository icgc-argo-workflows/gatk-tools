cwlVersion: v1.1
class: CommandLineTool
id: gatk-filter-mutect-calls

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-filter-mutect-calls:gatk-filter-mutect-calls.4.1.3.0-1.1'

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
  output_vcf:  # must ends with '.vcf.gz'
    type: string
    inputBinding:
      prefix: -O
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
  filtering_stats_output:  # output file name for filtering stats
    type: string?
    inputBinding:
      prefix: --filtering-stats

outputs:
  filtered_vcf:
    type: File
    outputBinding:
      glob: $(inputs.output_vcf)
    secondaryFiles: '.tbi'
  filtering_stats:
    type: File
    outputBinding:
      glob: $(inputs.filtering_stats_output)
