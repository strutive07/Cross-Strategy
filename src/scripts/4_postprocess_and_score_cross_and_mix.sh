MODEL=$1

F1=outputs/gsm8K_test_dt.gsm/$MODEL/cross_and_mix/n1_0.0_sg_raw_query_result.jsonl
F2=outputs/MATH-full_dt.math/$MODEL/cross_and_mix/n1_0.0_sg_raw_query_result.jsonl
F3=outputs/SVAMP_dt.svamp/$MODEL/cross_and_mix/n1_0.0_sg_raw_query_result.jsonl

python postprocess_rawouts.py process_cross_and_mix --dataset_type gsm --infile $F1
python postprocess_rawouts.py process_cross_and_mix --dataset_type math --infile $F2
python postprocess_rawouts.py process_cross_and_mix --dataset_type svamp --infile $F3

F1=outputs/gsm8K_test_dt.gsm/$MODEL/cross_and_mix/processed_cross_and_mix.jsonl
F2=outputs/MATH-full_dt.math/$MODEL/cross_and_mix/processed_cross_and_mix.jsonl
F3=outputs/SVAMP_dt.svamp/$MODEL/cross_and_mix/processed_cross_and_mix.jsonl

python score_processed.py score_cross_and_mix --ptn $F1
python score_processed.py score_cross_and_mix --ptn $F2
python score_processed.py score_cross_and_mix --ptn $F3
