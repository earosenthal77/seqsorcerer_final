## Contents

### Overview: 
This document dives deaper into the code files in the rnaseq_pipeline folder. For more general information on the repository, please see the README
document in the general project folder. This folder (```rnaseq_pipeline```) exists to specifiy which code files docker must use to create the docker image. 

```__init__.py```: This file sets the docker image version. This is required for the python/docker functionality. 

```__main__.py```: This file runs the main function defined in the ```cli.py``` file

```cli.py```: This file functions as the general run file for the pipeline. This file defines the ```main()``` function which tells python which functions to run, in what order, and how to store/save the outputs.

```check_tool.py```: This file checks the docker image and python to ensure all necessary tools and packages exist and are up to date 

```validation.py```: This file checks all inputs to make sure they meet requirements before running the pipeline. 

```trimming.py```: This file executes the trimming of the raw reads (.fastq files) and saves them as .fq files in a folder (```data/output/trimmed```).

```reference_genome.py```: This file takes the nih download (.gtf and .fna files) and creates the reference genome which is stored in .ht2l index files (```data/output/aligned_genome```)

```alignment.py```: This file executes the alingmnet portion which takes the trimmed reads and reference genome to create the .bam aligned file (```data/output/aligned_foleder_bamfiles)

```feature_counts.py```: This file executes the file step in the pipeline. It takes the aligned file and exports the gene counts as a .txt file for the user to review (```data/output/counts_folder```)

```fastq_trimmer.py```: This file is used to export the first 100 fastq sequences from raw files for testing purposes. These files are included in the repository for users to download to test and better understand the functionality of the pipeline. 



