#!/bin/bash
#SBATCH -n 1 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 0-00:05 # Runtime in D-HH:MM
#SBATCH -p serial_requeue # Partition to submit to
#SBATCH --mem=100 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH -o oatjob.out # File to which STDOUT will be written
#SBATCH -e oatjob.err # File to which STDERR will be written

oat04.stanford.edu
python3 ./rnn_train.py