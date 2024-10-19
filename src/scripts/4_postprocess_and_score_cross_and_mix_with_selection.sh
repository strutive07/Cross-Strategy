MODEL=$1

F1=outputs/gsm8K_test_dt.gsm/$MODEL/cross_and_mix_with_selection/n1_0.0_sg_raw_query_result.jsonl
F2=outputs/MATH-full_dt.math/$MODEL/cross_and_mix_with_selection/n1_0.0_sg_raw_query_result.jsonl

python postprocess_rawouts.py process_cross_and_mix --dataset_type gsm --infile $F1
python postprocess_rawouts.py process_cross_and_mix --dataset_type math --infile $F2

F1=outputs/gsm8K_test_dt.gsm/$MODEL/cross_and_mix_with_selection/processed_cross_and_mix.jsonl
F2=outputs/MATH-full_dt.math/$MODEL/cross_and_mix_with_selection/processed_cross_and_mix.jsonl

python score_processed.py score_cross_and_mix --ptn $F1
python score_processed.py score_cross_and_mix --ptn $F2
