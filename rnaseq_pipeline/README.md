## Contents

### Overview: 
This document dives deeper into the code files in the rnaseq_pipeline folder. For more general information on the repository, please see the README
document in the general project folder. This folder (```rnaseq_pipeline```) contains the Python files used to run the automated RNA-Seq pipeline inside the Docker image. These scripts define the workflow for input validation, read trimming, reference genome indexing, alignment, and gene-level read counting.

### Files:
```__init__.py```: This file marks the ```rnaseq_pipeline``` folder as a Python package. Allows files in this folder to be imported and used 

```__main__.py```: Runs the pipeline from the command line by calling the 'main()' function defined in `cli.py`.

```cli.py```: This file functions as the main run file for the pipeline. This file defines the ```main()``` function which tells python which functions to run, in what order, and how to store/save the outputs.

```check_tool.py```: This file checks that the required command0line tools and packages are available in the Docker image before the pipeline runs. 

```validation.py```: This file checks all inputs to make sure they meet requirements before running the pipeline. 

```trimming.py```: This file executes the trimming of the raw reads (.fastq.gz files) and saves them as .fq.gz files in a folder (```data/output/trimmed```).

```reference_genome.py```: This file takes the nih download (.gtf and .fna files) and creates a HISAT2 index which is stored in .ht2l files (```data/output/aligned_genome```).

```alignment.py```: This file executes the alignment portion which takes the trimmed reads and reference genome to create the .bam aligned file (```data/output/aligned_folder_bamfiles).

```feature_counts.py```: This file executes the file step in the pipeline. It takes the aligned file and exports the gene counts as a .txt file for the user to review (```data/output/counts_folder```).

```fastq_trimmer.py```: This file is used to export the first 100 fastq sequences from raw files for testing purposes. These files are included in the repository for users to download to test and better understand the functionality of the pipeline. 



