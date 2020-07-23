cwlVersion: v1.1
class: CommandLineTool
id: gatk-get-pileup-summaries

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-get-pileup-summaries:gatk-get-pileup-summaries.4.1.8.0-2.0'

baseCommand: [ 'gatk-get-pileup-summaries.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  ref_fa:
    type: File?
    inputBinding:
      prefix: -R
    secondaryFiles: ['.fai', '^.dict']
  seq_file:
    type: File
    inputBinding:
      prefix: -I
    secondaryFiles: ['.bai?', '.crai?']
  variants:
    type: File
    inputBinding:
      prefix: -V
    secondaryFiles: ['.tbi']
  intervals:
    type: File
    inputBinding:
      prefix: -L

outputs:
  pileups_table:
    type: File
    outputBinding:
      glob: "*.pileups_metrics.txt"
