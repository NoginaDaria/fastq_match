# fastq_match
FASTQ match is a simple way to fix your paired end fastq or fastq.gz files

### Getting Started
You can often face a problem of inequality of reads number in paired fastq files. This script can solve this and help you to get rid of singletons. 
Of course, it's not a groundbreaking issue. The faster version of solving this problem is https://github.com/linsalrob/fastq-pair, which I highly recommend to use. But this solution doesn't work with gzipped fastq files. So, if you need to save space or just too lazy to gunzip your files (like me) you are free to use this script. 

### Prerequisites
python3

### Running

```
python fastq_match.py
```
Then it will ask you to enter the full path to the directory with fastq files and to enter either y or n depending on which file format do you use.

