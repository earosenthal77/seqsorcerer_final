input_file = "input.fastq"
output_file = "first_100_sequences.fastq"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for i in range(100):
        # Read one FASTQ record (4 lines)
        record = [infile.readline() for _ in range(4)]
        
        # Stop if we hit end of file
        if not record[0]:
            break
        
        # Write the record
        outfile.writelines(record)

print("First 100 FASTQ sequences exported!")