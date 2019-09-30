cwlVersion: v1.1
class: CommandLineTool
id: gatk-merge-vcfs

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-tools/gatk-merge-vcfs:gatk-merge-vcfs.4.1.3.0-1.0'

baseCommand: [ 'gatk-merge-vcfs.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  input_vcf:  # input VCF file(s)
    type: File[]
    inputBinding:
      prefix: -I
  output_name:  # output file name, must ends with .vcf.gz
    type: string
    inputBinding:
      prefix: -O

outputs:
  output_vcf:
    type: File
    outputBinding:
      glob: $(inputs.output_name)
