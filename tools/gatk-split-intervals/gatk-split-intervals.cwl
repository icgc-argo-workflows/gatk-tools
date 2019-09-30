cwlVersion: v1.1
class: CommandLineTool
id: gatk-split-intervals

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-split-intervals:gatk-split-intervals.4.1.3.0-1.0'

baseCommand: [ 'gatk-split-intervals.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  ref_fa:
    type: File
    inputBinding:
      prefix: -R
    secondaryFiles: ['.fai', '^.dict']
  intervals:
    type: File?
    inputBinding:
      prefix: -L
  scatter_count:
    type: int
    inputBinding:
      prefix: --scatter
  split_intervals_extra_args:  # placeholder for now
    type: string?
    inputBinding:
      prefix: --extra-args

outputs:
  interval_files:
    type: File[]
    outputBinding:
      glob: '*.interval_list'
