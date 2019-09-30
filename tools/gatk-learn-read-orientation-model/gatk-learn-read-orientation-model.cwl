cwlVersion: v1.1
class: CommandLineTool
id: gatk-learn-read-orientation-model

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-learn-read-orientation-model:gatk-learn-read-orientation-model.4.1.3.0-1.0'

baseCommand: [ 'gatk-learn-read-orientation-model.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  input_f1r2_tar_gz:  # input f1r2_tar_gz file(s)
    type: File[]
    inputBinding:
      prefix: -I
  output_name:
    type: string
    inputBinding:
      prefix: -O

outputs:
  artifact_prior_table:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
