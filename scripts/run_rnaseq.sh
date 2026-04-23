#!/bin/bash

# --- USER CONFIGURATION ---
# $(pwd) dynamically finds the path to your 'seqsorcerer_final' folder
BASE_DIR=$(pwd)

# Change these paths to point to your actual data on your computer
READS_DIR="$BASE_DIR/data/testing"
REF_DIR="$BASE_DIR/ncbi_dataset/ncbi_dataset/data/GCF_017654675.1"
GENOME_FASTA="$BASE_DIR/ncbi_dataset/ncbi_dataset/data/GCF_017654675.1/GCF_017654675.1_Xenopus_laevis_v10.1_genomic.fna"
ANNOTATION_GTF="$BASE_DIR/ncbi_dataset/ncbi_dataset/data/GCF_017654675.1/genomic.gtf"
OUTPUT_DIR="$BASE_DIR/data/output"

# --- PIPELINE EXECUTION ---
# This matches the "docker run pattern" from the handoff
docker run --rm \
  --mount type=bind,src="$READS_DIR",dst=/data/reads,ro \
  --mount type=bind,src="$REF_DIR",dst=/data/reference,ro \
  --mount type=bind,src="$OUTPUT_DIR",dst=/data/output \
  rnaseq-pipeline:1.0 \
  --fastq-dir /data/reads \
  --reference "/data/reference/$(basename $GENOME_FASTA)" \
  --gtf "/data/reference/$(basename $ANNOTATION_GTF)" \
  --outdir /data/output