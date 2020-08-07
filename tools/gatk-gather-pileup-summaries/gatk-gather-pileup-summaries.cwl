cwlVersion: v1.1
class: CommandLineTool
id: gatk-gather-pileup-summaries

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-gather-pileup-summaries:gatk-gather-pileup-summaries.4.1.8.0-2.0'

baseCommand: [ 'gatk-gather-pileup-summaries.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  ref_dict:  # input reference sequence .dict file
    type: File
    inputBinding:
      prefix: -D
  input_pileup:  # input pipeup summary table(s)
    type: File[]
    inputBinding:
      prefix: -I

outputs:
  merged_pileup:
    type: File
    outputBinding:
      glob: "*.pileups_metrics.tsv"
