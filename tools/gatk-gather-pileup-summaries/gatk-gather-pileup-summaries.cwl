cwlVersion: v1.1
class: CommandLineTool
id: gatk-gather-pileup-summaries

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-gather-pileup-summaries:gatk-gather-pileup-summaries.4.1.3.0-1.0'

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
  output_name:  # output file name, must ends with .tsv
    type: string
    inputBinding:
      prefix: -O

outputs:
  merged_pileup:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
