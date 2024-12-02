#!/bin/bash
MODEL=$1

run_process()
{
    echo "first parameter : "$1
    echo "second parameter : "$2
    echo "second parameter : "$3

    ptn1="$2/$3/n1_0.0_sg_raw_query_result.jsonl"
    ptn2="$2/$3/processed_cross_and_mix.jsonl"

    python postprocess_rawouts.py process_cross_and_mix --dataset_type $1 --infile $ptn1
    python score_processed.py score_cross_and_mix --ptn $ptn2
}

run_process "gsm" "outputs/gsm8K_test_dt.gsm/$MODEL" "cross_and_mix"
run_process "math" "outputs/MATH-full_dt.math/$MODEL" "cross_and_mix"
run_process "svamp" "outputs/SVAMP_dt.svamp/$MODEL" "cross_and_mix"