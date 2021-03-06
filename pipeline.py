#!/usr/bin/env python

# ~~~~~~ LOAD PACKAGES ~~~~~ #
# system packages
import sys
import os

# pipeline packages
from base_classes import *
from pipeline_classes import *
from pipeline_functions import *

def build_pipeline_task_list(sampleID):
    '''
    Build the tasks list of tasks for the pipeline to run
    '''
    # ~~~~~~ CREATE TASK OBJECTS ~~~~~ #
    foo = printFoo(sampleID = sampleID)
    fastqc = runFastQC(input_dir = 'input', sampleID = sampleID) #
    align_bowtie2 = alignBowtie2(input_dir = 'input', sampleID = sampleID)
    do_python = doPythonCode(sampleID = sampleID)
    convert_fastq = convertFastq2Txt(sampleID = sampleID)
    bam_to_bed = bamToBed(sampleID = sampleID, input_dir = align_bowtie2.output_dir) # input_task = align_bowtie2
    bam_to_bedgraph = bamToBedgraph(sampleID = sampleID, input_dir = align_bowtie2.output_dir)
    bed_to_BigBed = bedToBigBed(sampleID = sampleID, input_dir = bam_to_bed.output_dir)
    bedgraph_to_bigwig = bedgraphToBigWig(sampleID = sampleID, input_dir = bam_to_bedgraph.output_dir)

    # ~~~~~~ BUILD TASK LIST ~~~~~ #
    task_list = [
    foo,
    fastqc,
    align_bowtie2,
    bam_to_bedgraph,
    bam_to_bed,
    bed_to_BigBed,
    bedgraph_to_bigwig,
    do_python,
    convert_fastq
    ]
    # my_debugger(locals().copy())
    return(task_list)

if __name__ == "__main__":
    sampleID = "test2"
    # my_debugger(globals().copy())
    task_list = build_pipeline_task_list(sampleID)
    # ~~~~~~ RUN THE TASKS ~~~~~ #
    run_pipeline(task_list, sampleID)
