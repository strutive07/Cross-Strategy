MODEL=$1

F1=outputs/gsm8K_test_dt.gsm/$MODEL/processed_indiv.jsonl
F2=outputs/SVAMP_dt.svamp/$MODEL/processed_indiv.jsonl
F3=outputs/MATH-full_dt.math/$MODEL/processed_indiv.jsonl

for F in $F1 $F2 $F3; do
    python run_sg.py --indiv_processed_jslf $F --backbone $MODEL
done
