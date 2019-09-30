cwlVersion: v1.1
class: CommandLineTool
id: gatk-calculate-contamination

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-tools/gatk-calculate-contamination:gatk-calculate-contamination.4.1.3.0-1.0'

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
  segmentation_output:
    type: string
    inputBinding:
      prefix: --tumor-segmentation
  contamination_output:
    type: string
    inputBinding:
      prefix: -O

outputs:
  segmentation_table:
    type: File
    outputBinding:
      glob: $(inputs.segmentation_output)
  contamination_table:
    type: File
    outputBinding:
      glob: $(inputs.contamination_output)
