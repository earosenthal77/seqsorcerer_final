# seqsorcerer_final
Welcome to SeqSorcerer, an automated RNA-Sequencing pipeline!
## Purpose
SeqSorcerer was developed as an automated RNA-Seq processing pipeline designed to reduce manual intervention while preserving the established analytical workflow used in the Saha lab at William & Mary. Rather than changing any preexisting RNA-Seq methods, SeqSorcerer encapsulates the same major processing steps within a structured and reproducible framework. The pipeline integrates quality trimming, reference genome preparation, sequence alignment, and gene quantification using commonly used RNA-Seq tools, including Trim Galore, HISAT2, Samtools, and featureCounts. Although originally designed for use in the Saha lab, SeqSorcerer can be easily adapted for alternate RNA-Seq projects.

## Quick-Start Guide
### Prerequisites:
RNA-Seq is a computationally expensive pipeline, regardless of automation. The user needs 16GB+ RAM allocated to Docker to run SeqSorcerer.
### 1. Clone the seqsorcerer_final Repository
### 2. Download raw read FASTQ files and reference genome files
Have FASTQ files downloaded locally on your computer      
Download the reference genome for your species of choice            
For example, this project uses X. laevis reference genome V10.1 from the National Institutes of Health (NIH) website          
https://www.ncbi.nlm.nih.gov/assembly/9809711
### 3. Create data folder with Raw Reads and Reference Genome
Create the data folder within the downloaded repository.
### 4. Edit Config File Directory Paths to Local File Paths
Open the run_rnaseq.sh config file and change the five file paths to direct the pipeline to the files in your data folder.       
The five required paths are:
1. ```READS_DIR = ```
2. ```REF_DIR = ```
3. ```GENOME_FASTA = ```
4. ```ANNOTATION_GTF =```
5. ```OUTPUT_DIR = ```
### 5. Download Docker Desktop and Create Account
Download at this link: https://www.docker.com/products/docker-desktop/        
Create a Docker account with a username and password.
** To allot more RAM to Docker: go into Docker settings, under Resources, and expand memory limit and CPU slider bar
### 6. Build Docker Image
Use terminal to set your working directory to the seqsorcerer_final repository      
Build Docker image with this command: ```docker build -t rnaseq-pipeline:1.0 .```
### 7. Give the .sh Config File Permission to Run
Copy and paste this code into your terminal: ```chmod +x scripts/run_rnaseq.sh```
### 8. Run the .sh Config File
Copy and paste this code into your terminal: ```./scripts/run_rnaseq.sh```

## Contents
This section will provide a high level description of the contents of the repository. For more detailed information on the subfolders, please see the README files in the individual folders. 

1. The ```.gitignore``` file tells github to disregard specific folders/files when uploading to the web. The ignored folders include: the data folder and ncbi_dataset folder which contain the raw reads and files downloaded from the nih. These files are extremely large and this data should be acquired by the user. 

1. The ```.dockerignore``` tells docker which files ito exclude when building the image. With the current setup, docker only has access to ```env.yaml```, ```rnaseq_pipeline\```, and```Dockerfile```.
      - ```Dockerfile```: You will see this file in your working directory after creating the Docker image. This downloads Micromamba, tells Micromamba which bioinformatics tools to download, and copies project files from your er into the Docker container.
      - ```env.yaml```: tells docker and micromamba which bioinformatics tools are required and the code dependencies.
      - ```rnaseq_pipeline\``` is the folder containing the pipeline scripts. It contains individual scripts for each step in the pipeline as well as the ```cli.py``` file which runs each step in the correct order. Please see the individual README for more information.

2. ```pyproject.toml```: This is the python configuration file. It defines project metadata and package settings used by the Python environment.

3. ```scripts```: This folder contains the ```run_rnaseq.sh``` file. 
      - ```run_rnaseq.sh```: This is a shell script that contains a sequence of commands to run the pipeline. This file is also essential to the automation aspect of the pipeline. Additionally, this file allows users to define the working directories for the data inputs and pipeline outputs.

## Testing
If you would like to test SeqSorcerer before running on full FASTQ files, a ```fastq_trimmer.py``` file is available within the ```rnaseq_pipeline``` folder. This will trim any gzipped file of the format .fastq.gz to the first 100 reads. This provides a shortened fastq file allowing for a shortened run-through of the pipeline.           
Two paired, 100 read files are also available for testing.
Note: testing files must follow the same naming conventions expected by the pipeline.        
## Validation
1. Verifiable Success: The pipeline completes a successful run when a ```.bam``` file is produced in the output folder and the ```featureCounts``` summary report shows a 'Successfully assigned' rate > 0%.
2. Runtime Improvements:          
         - Previously: ~30-45 minutes of active, hands-on time (check steps, typing commands,                 fixing errors) per file       
         - SeqSorcerer: <2 mins of hands-on time (editing the .sh file) per batches of files
3. Failure Handling: Before running, the pipeline checks all tools and their versions. Paired read files are checked to make sure both R1 and R2 files are provided. The system also checks for existing trimmed files or gene indices. If the pipeline is interrupted, it can resume rather than restart.

## In Progress Future Directions
# Customizable Parameters:
Currently, the pipeline is optimized for _Xenopus laevis_ RNA-Sequencing reads from the Saha lab. Soon, a feature will be available allowing users to change the parameters of each tool (e.g. type of strandness).  

