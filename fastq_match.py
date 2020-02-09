import os
import gzip
import shutil
from tqdm import tqdm

path_to_files = input('Path to files: \t') #'/Users/daria/Documents/scripts/t1d/data_kostic/fastq_test/'

if not os.path.isdir(path_to_files):
    print('Sorry, incorrect input. Please, try again')
    path_to_files = input('Path to files: \t')

if path_to_files[-1] != '/':
    path_to_files = path_to_files + '/'

to_gzip = input('.fastq.gz [y] or .fastq [n] \t')

if to_gzip not in ['y', 'n']:
    print('Sorry, incorrect input. Please, try again')
    to_gzip = input('.fastq.gz [y] or .fastq [n] \t')

# get uniq prefixes of files in the folder
prefixes = set(filename.split('_')[0] for filename in os.listdir(path_to_files))

def get_id_list(fastq_file):

    '''
    Get set of all ids from fastq file
    '''

    id_list = set()
    line_num = 0

    if to_gzip in ['y', 'n']:
        pass
    else:
        return 'Error'

    if to_gzip == 'y':
        for line in gzip.open(fastq_file, mode='rb'):
            line_decoded = line.decode("utf-8").strip('\n')
            if (line_num % 4) == 0:
                id_list.add(line_decoded[:-1])
            line_num += 1

        try:
            try_file = gzip.open(fastq_file, mode='rb')
        except OSError:
            with open(fastq_file, 'rb') as f_in:
                with gzip.open(fastq_file+'_tmp', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(fastq_file)
            os.rename(fastq_file + '_tmp', fastq_file)

    elif to_gzip == 'n':
        with open(fastq_file, 'r') as f:
            for line in f:
                line = line.strip('\n')
                if (line_num % 4) == 0:
                    id_list.add(line[:-1])
                line_num += 1


    return id_list

def write_corrected(prefix, fastq_file):
    '''
    Write a new fastq file without mismatched ids. Removes an old file.
    '''

    if to_gzip == 'y':
        with gzip.open(fastq_file, 'rb') as init_fastq:
            with gzip.open(fastq_file + '_tmp', 'wb') as new_fastq:
                for line in init_fastq:
                    line = line.decode("utf-8").strip('\n')
                    if line[:-1] in mismatch_samples.get(prefix):
                        for i in range(3):
                            tmp = init_fastq.readline()
                    else:
                        new_fastq.write((line+'\n').encode())


    elif to_gzip == 'n':
        with open(fastq_file, 'r') as init_fastq:
            with open(fastq_file + '_tmp', 'w') as new_fastq:
                for line in init_fastq:
                    line = line.strip('\n')
                    if line[:-1] in mismatch_samples.get(prefix):
                        for i in range(3):
                            next(init_fastq)
                    else:
                        new_fastq.write(line+'\n')

    os.remove(fastq_file)
    os.rename(fastq_file + '_tmp', fastq_file)

mismatch_samples = dict() # prefix: (mismatched ids)

print('Searching for mismatches...')

with tqdm(range(len(prefixes))) as pbar:
    for prefix in prefixes:

        try:
            fastq1, fastq2 = [(path_to_files + filename) for filename in os.listdir(path_to_files) if filename.startswith(prefix)]
        except:
            print(f'You have downloaded not paired files!\nNeed pair for {prefix}')
            print('Keep searching for mismatches...')
            continue

        id_list1, id_list2 = get_id_list(fastq1), get_id_list(fastq2)
        mismatched = id_list1.symmetric_difference(id_list2)
        if len(mismatched) > 0:
            mismatch_samples[prefix] = mismatched

        pbar.update(1)

print('Treating sick files...')
with tqdm(range(len(mismatch_samples.keys()))) as pbar:
    for prefix in mismatch_samples.keys():

        fastq1, fastq2 = [(path_to_files + filename) for filename in os.listdir(path_to_files) if filename.startswith(prefix)]

        write_corrected(prefix, fastq1)
        write_corrected(prefix, fastq2)

        pbar.update(1)


print(f'Total number of fixed files is {len(mismatch_samples.keys())*2}\nTotal number of removed reads is {sum([len(i) for i in mismatch_samples.values()])}')
