# seqsorcerer_final
Welcome to SeqSorcerer, an automated RNA-Sequencing pipeline!
## Purpose
SeqSorcerer was developed as an automated RNA-Seq processing pipeline designed to reduce manual intervention while preserving the established analytical workflow used in the Saha lab at William & Mary. Rather than changing any preexisting RNA-Seq methods, SeqSorcerer encapsulates the same major processing steps within a structured and reproducible framework. The pipeline integrates quality trimming, reference genome preparation, sequence alignment, and gene quantification using commonly used RNA-Seq tools, including Trim Galore, HISAT2, Samtools, and featureCounts. Although originally designed for use in the Saha lab, SeqSorcerer can be easily adapted for alternate RNA-Seq projects.

## Quick-Start Guide
### 1. Clone the seqsorcerer_final Repository
### 2. Download raw read FASTQ files and reference genome files
Have FASTQ files downloaded locally on your computer      
Download the reference genome for your species of choice            
For example, this project uses X. laevis reference genome V10.1 from the National Institute of Health (NIH) website          
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
** Note: go into Docker settings, under Resources, and expand memory limit slider bar
### 6. Build Docker Image
Use terminal to set your working directory to the seqsorcerer_final repository      
Build Docker image with this command: ```docker build -t rnaseq-pipeline:1.0 .```
### 7. Give the .sh Config File Permission to Run
Copy and paste this code into your terminal: ```chmod +x scripts/run_rnaseq.sh```
### 8. Run the .sh Config File
Copy and paste this code into your terminal: ```./scripts/run_rnaseq.sh```

## Contents
This section will provide a high level description of the contents of the repository. For more detailed information on the subfolders, please see the README files in the individual folders. 

1. The ```.gitignore``` file tells github to disregard specific folders/files when uploading to the web. The ignored folders include: the data folder and ncbi_dataset folder which contain the raw reads and files downloaded from the nih. These files are extremely large and this data should be aquired by the user. 

1. The ```.dockerignore``` tells docker which files it can to access to build the image and run the pipeline. With the current setup, docker only has access to ```env.yaml```, ```rnaseq_pipeline\```, and```Dockerfile```.
      - ```Dockerfile```: You will see this file in your working directory after creating the Docker image. This downloads Micromamba, tells Micromamba which bioinformatics tools to download, and copies project files from your computer into the Docker container.
      - ```env.yaml```: tells docker and micromamba which bioinformatics tools are required and the code dependencies.
      - ```rnaseq_pipeline\``` is the folder containing the pipeline scripts. It contains individual scripts for each step in the pipeline as well as the ```cli.py``` file which runs each step in the correct order. Please see the individual README for more information.

2. ```docker-compose.yml```: This file is used to configure the entire pipeline to allow users to type one single command into the terminal as opposed to running many individual commands. This file is essential to the automation aspect of the pipeline. 

3. ```pyproject.toml```: This is the python configuration file. It allows our project to use python in combination with the python3.12 folder. 

4. ```scripts```: This folder contains the ```run_rnaseq.sh``` file. 
      - ```run_rnaseq.sh```: This is a shell script that contains a sequence of commands to run the pipeline. This file is also essential to the automation aspect of the pipeline. Additionally, this file allows users to define the working directories for the data inputs and pipeline outputs. 

