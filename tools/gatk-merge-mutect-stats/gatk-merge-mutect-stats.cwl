cwlVersion: v1.1
class: CommandLineTool
id: gatk-merge-mutect-stats

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-merge-mutect-stats:gatk-merge-mutect-stats.4.1.3.0-1.0'

baseCommand: [ 'gatk-merge-mutect-stats.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  input_stats:  # input mutect stats file(s)
    type: File[]
    inputBinding:
      prefix: -I
  output_name:  # output file name, must ends with .stats
    type: string
    inputBinding:
      prefix: -O

outputs:
  merged_stats:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
