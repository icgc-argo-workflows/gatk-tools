cwlVersion: v1.1
class: CommandLineTool
id: gatk-mutect2

requirements:
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/gatk-mutect2:gatk-mutect2.4.1.3.0-1.3'

baseCommand: [ 'gatk-mutect2.py' ]

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
  tumour_reads:
    type: File
    inputBinding:
      prefix: --tumour-reads
    secondaryFiles: ['.bai?', '.crai?']
  normal_reads:
    type: File?
    inputBinding:
      prefix: --normal-reads
    secondaryFiles: ['.bai?', '.crai?']
  output_vcf:
    type: string
    inputBinding:
      prefix: -O
  germline_resource:
    type: File?
    inputBinding:
      prefix: --germline-resource
    secondaryFiles: ['.idx?', '.tbi?']
  pon:
    type: File?
    inputBinding:
      prefix: -pon
    secondaryFiles: ['.idx?', '.tbi?']
  intervals:
    type: File?
    inputBinding:
      prefix: -L
  bam_output:
    type: string?
    inputBinding:
      prefix: --bam-output
  f1r2_tar_gz:
    type: string?
    inputBinding:
      prefix: --f1r2-tar-gz
  m2_extra_args:  # placeholder for now
    type: string?
    inputBinding:
      prefix: --extra-args

outputs:
  unfiltered_vcf:
    type: File
    outputBinding:
      glob: "*$(inputs.output_vcf)"
    secondaryFiles: [.tbi]
  mutect_stats:
    type: File
    outputBinding:
      glob: "*$(inputs.output_vcf).stats"
  bam_output:
    type: ['null', File]
    outputBinding:
      glob: "*$(inputs.bam_output)"
    secondaryFiles: [.bai]
  f1r2_counts:
    type: ['null', File]
    outputBinding:
      glob: "*$(inputs.f1r2_tar_gz)"
