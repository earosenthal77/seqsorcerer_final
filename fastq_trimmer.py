import gzip

input_file = "/Users/margaretsaha/Desktop/Molly2024/rawreads/S18_Sib/21_L18_sib_170501_R2_001.fastq.gz"
output_file = "/Users/margaretsaha/Desktop/Molly2024/rawreads/S18_Sib/S18_Sib_R2_first100.fastq"

with gzip.open(input_file, "rt") as infile, open(output_file, "w") as outfile:
    for i in range(100):
        # Read one FASTQ record (4 lines)
        record = [infile.readline() for _ in range(4)]
        
        # Stop if we hit end of file
        if not record[0]:
            break
        
        # Write the record
        outfile.writelines(record)

print("First 100 FASTQ sequences exported!")