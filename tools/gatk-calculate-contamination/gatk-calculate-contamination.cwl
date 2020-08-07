cwlVersion: v1.1
class: CommandLineTool
id: gatk-calculate-contamination

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-calculate-contamination:gatk-calculate-contamination.4.1.8.0-2.0'

baseCommand: [ 'gatk-calculate-contamination.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  tumour_pileups:
    type: File
    inputBinding:
      prefix: -I
  normal_pileups:
    type: File?
    inputBinding:
      prefix: -matched
  tumour_normal:
    type: string?
    inputBinding:
      prefix: -s

outputs:
  segmentation_table:
    type: File
    outputBinding:
      glob: "*.segmentation_metrics"
  contamination_table:
    type: File
    outputBinding:
      glob: "*.contamination_metrics"
