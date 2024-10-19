#!/bin/sh
# Please modify OPENAI_API_BASE, OPENAI_API_KEY in this script and run script.

set -e

MODEL_NAME=$1

export OPENAI_API_BASE=$OPENAI_API_BASE
export OPENAI_API_KEY=$OPENAI_API_KEY

sh scripts/0_run_indiv.sh $MODEL_NAME
sh scripts/1_run_postprocess_indiv.sh $MODEL_NAME
sh scripts/2_score_indiv.sh $MODEL_NAME
sh scripts/3_run_cross_and_mix.sh $MODEL_NAME
sh scripts/3_run_cross_and_mix_with_selection.sh $MODEL_NAME
sh scripts/3_run_sg.sh $MODEL_NAME
sh scripts/4_postprocess_and_score_cross_and_mix_with_selection.sh $MODEL_NAME
sh scripts/4_postprocess_and_score_cross_and_mix.sh $MODEL_NAME
sh scripts/4_postprocess_and_score_sg.sh $MODEL_NAME
python print_score.py