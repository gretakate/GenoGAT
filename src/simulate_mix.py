import os
import itertools
from tqdm import tqdm
import subprocess

def generate_read_fragments_with_badread(fasta_file, quantity=50, length_mean=15000, length_std=13000):
    os.makedirs('data/intermediate_files', exist_ok=True)
    reads_outfile = f"data/intermediate_files/{fasta_file.split('/')[-1].split('_')[0]}_reads.fq"
    # print(f"Saving reads file to {reads_outfile}")
    command = [
        "badread",
        "simulate",
        "--reference", f"{fasta_file}",
        "--quantity", f"{quantity}x",
        "--error_model", "nanopore2023",
        "--qscore_model", "nanopore2023",
        "--glitches", "0,0,0",
        "--junk_reads", "0",
        "--random_reads", "0",
        "--chimeras", "0",
        "--identity", "30,3",
        "--length", f"{length_mean},{length_std}",
        "--start_adapter_seq", "",
        "--end_adapter_seq", "",
    ]

    # Run the command with redirection
    with open(reads_outfile, "w") as outfile:  # Open output file for writing
        subprocess.run(command, stdout=outfile, stderr=subprocess.PIPE)  # Redirect stdout and capture stderr

    return reads_outfile

def combine_fasta_with_class(files: list[str], output_file: str):
  """
  Combines two fasta files into one, adding class label to each sequence header.
  """
  with open(output_file, 'w') as outfile:
    # Open and read each file
    for i in range(len(files)):
      file_i = files[i]
      with open(file_i, 'r') as infile1:
        for line in infile1:
          if line.startswith('@'):
            # Add class label to header
            outfile.write(f"@class{i}_" + line[1:])
          else:
            outfile.write(line)
            
def generate_simulated_mixes(read_path, save_path, num_contributors=2):
  all_files = os.listdir(read_path)
  all_files = [os.path.join(read_path, file) for file in all_files]
  combinations = list(itertools.combinations(all_files, num_contributors))
  for contributor_files in tqdm(combinations):
    try:
      reads_files = [generate_read_fragments_with_badread(raw_file) for raw_file in contributor_files]
      name_fragmented = [file.split('/')[-1].split('.fasta')[0] for file in contributor_files]
      combined_name = '_'.join(name_fragmented)
      output_file = os.path.join(save_path, f"mix_{combined_name}.fq")
      combine_fasta_with_class(reads_files, output_file)
    except:
      print(f"Error with {contributor_files}")
      
if __name__=="__main__":
    RAW_TRAINING_SAMPLES_PATH = 'data/raw_covid_rna_train'
    RAW_TEST_SAMPLES_PATH = 'data/raw_covid_rna_test'

    TRAINING_DATA_PATH = 'data/training_mixes'
    TEST_DATA_PATH = 'data/test_mixes'

    os.makedirs(TRAINING_DATA_PATH, exist_ok=True)
    os.makedirs(TEST_DATA_PATH, exist_ok=True)
    
    generate_simulated_mixes(RAW_TRAINING_SAMPLES_PATH, TRAINING_DATA_PATH, num_contributors=2)
    generate_simulated_mixes(RAW_TEST_SAMPLES_PATH, TEST_DATA_PATH, num_contributors=2)
    
    