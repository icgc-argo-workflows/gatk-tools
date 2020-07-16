[![Build Status](https://travis-ci.org/icgc-argo/gatk-tools.svg?branch=master)](https://travis-ci.org/icgc-argo/gatk-tools)
# Dockerized GATK Tools

This repository keeps a collect of GATK tools. All tools are dockerized and wrapped using Nextflow (NF)
workflow language.

Every tool is self-sufficient, can be independently developed, tested, released and used. This clean isolation allows maximum flexibility, maintainability and portability.

These tools are building blocks to create multi-step data analysis workflows as needed, like the
workflows here: https://github.com/icgc-argo/gatk-mutect2-variant-calling

## Development
As tools are meant to be independent from each other, arguably a better choice is to
develop each tool using its own source control repository and container image. In
reality, it's undesirable to have to manage too many repositories, so we ended up
with choosing to use one repository for many tools. Despite sharing the same repository, in
tools development, we still want to follow good practices to ensure as much as possible
tools are independent. See more details: https://github.com/icgc-argo/dna-seq-processing-tools/blob/master/README.md
