cwlVersion: v1.1
class: CommandLineTool
id: gatk-filter-alignment-artifacts

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-tools/gatk-filter-alignment-artifacts:gatk-filter-alignment-artifacts.4.1.3.0-1.0'

baseCommand: [ 'gatk-filter-alignment-artifacts.py' ]

inputs:
  jvm_mem:
    type: int?
    inputBinding:
      prefix: -j
  bwa_mem_index_image:
    type: File
    inputBinding:
      prefix: --bwa-mem-index-image
  tumour_seq:
    type: File  # BAM/SAM/CRAM file containing tumour reads
    inputBinding:
      prefix: -I
    secondaryFiles: ['.bai', '.crai']
  input_vcf:
    type: File  # A VCF file containing variants
    inputBinding:
      prefix: -V
    secondaryFiles: '.tbi'
  output_vcf:
    type: string
    inputBinding:
      prefix: -O

outputs:
  filtered_vcf:
    type: File
    outputBinding:
      glob: $(inputs.output_vcf)
