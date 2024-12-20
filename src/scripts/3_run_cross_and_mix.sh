MODEL=$1

F1=outputs/gsm8K_test_dt.gsm/$MODEL/processed_indiv.jsonl
F2=outputs/MATH-full_dt.math/$MODEL/processed_indiv.jsonl
F3=outputs/SVAMP_dt.svamp/$MODEL/processed_indiv.jsonl

python run_cross_and_mix.py --indiv_processed_jslf $F1 --backbone $MODEL --with_selection False
python run_cross_and_mix.py --indiv_processed_jslf $F2 --backbone $MODEL --with_selection False
python run_cross_and_mix.py --indiv_processed_jslf $F3 --backbone $MODEL --with_selection False