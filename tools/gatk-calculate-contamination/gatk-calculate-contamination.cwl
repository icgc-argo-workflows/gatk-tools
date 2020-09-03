cwlVersion: v1.1
class: CommandLineTool
id: gatk-calculate-contamination

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-calculate-contamination:gatk-calculate-contamination.4.1.8.0-2.1'

baseCommand: [ 'gatk-calculate-contamination.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  seq_pileups:
    type: File
    inputBinding:
      prefix: -I
  matched_pileups:
    type: File?
    inputBinding:
      prefix: -matched

outputs:
  segmentation_table:
    type: File
    outputBinding:
      glob: "*.segmentation_metrics"
  contamination_table:
    type: File
    outputBinding:
      glob: "*.contamination_metrics"
