import io
import os
import glob

import pandas as pd
from tabulate import tabulate


def load_scores():
    files = glob.glob("outputs/*/*/processed_indiv_scored.md")

    df_dict = {}
    
    for file in files:
        dataset_name, model_name, df = read_md(file)
        if dataset_name not in df_dict:
            df_dict[dataset_name] = {}
            
        df_dict[dataset_name][model_name] = df

    for dataset_name in df_dict:
        df_dict[dataset_name] = pd.concat(df_dict[dataset_name].values()).sort_values(by=["model_name"], ascending=[True]) 
    return df_dict

def get_score_from_text(text):
    for line in text.split('\n'):
         if 'total:' in line:
             return line.replace('total:', '').strip().split(' ')
    return 0

def load_sg(dataset_name, model_name):
    fname = f'outputs/{dataset_name}/{model_name}/simple_greedy/processed_sg_scored.txt'
    if os.path.exists(fname):
        with open(fname) as f:
            return ' '.join(get_score_from_text(f.read()))
    else:
        return ''

def load_rims(dataset_name, model_name):
    fname = f'outputs/{dataset_name}/{model_name}/rims/*/processed_rims_scored.txt'

    fnames = glob.glob(fname)
    max_score = 0
    status = ''
    
    for fname in fnames:
        with open(fname) as f:
            score, status = get_score_from_text(f.read())
            if float(score) >= max_score:
                max_score = float(score)

    return f'{max_score} {status}'

def load_rims_disable_hinting(dataset_name, model_name):
    fname = f'outputs/{dataset_name}/{model_name}/rims/*/processed_disable_hinting_rims_scored.txt'

    fnames = glob.glob(fname)
    max_score = 0
    status = ''
    
    for fname in fnames:
        with open(fname) as f:
            score, status = get_score_from_text(f.read())
            if float(score) >= max_score:
                max_score = float(score)

    return f'{max_score} {status}'

def load_cross_and_mix(dataset_name, model_name, suffix=""):
    fname = f'outputs/{dataset_name}/{model_name}/cross_and_mix{suffix}/processed_cross_and_mix_scored.txt'

    fnames = glob.glob(fname)
    max_score = 0
    status = ''
    
    for fname in fnames:
        with open(fname) as f:
            score, status = get_score_from_text(f.read())
            if float(score) >= max_score:
                max_score = float(score)

    return f'{max_score} {status}'

def load_cross_and_mix_with_selection(dataset_name, model_name):
    fname = f'outputs/{dataset_name}/{model_name}/cross_and_mix_with_selection/processed_cross_and_mix_scored.txt'

    fnames = glob.glob(fname)
    max_score = 0
    status = ''
    
    for fname in fnames:
        with open(fname) as f:
            score, status = get_score_from_text(f.read())
            if float(score) >= max_score:
                max_score = float(score)

    return f'{max_score} {status}'

def read_md(fname):
    with open(fname) as f:
        markdown_table = f.read()
    df = pd.read_table(io.StringIO(markdown_table), sep='|', header=0, index_col=0)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.reset_index().drop(columns=['index', '']).drop(0)

    dataset_name = fname.split('/')[1]
    model_name = fname.split('/')[2]
    
    df['model_name'] = [model_name]
    df['simple greedy'] = [str(load_sg(dataset_name, model_name))]
    
    df['cross_and_mix'] = [str(load_cross_and_mix(dataset_name, model_name))]
    # df['cross_and_mix_cot_pal'] = [str(load_cross_and_mix(dataset_name, model_name, "_cot_pal"))]
    # df['cross_and_mix_cot_p2c'] = [str(load_cross_and_mix(dataset_name, model_name, "_cot_p2c"))]
    # df['cross_and_mix_p2c_pal'] = [str(load_cross_and_mix(dataset_name, model_name, "_p2c_pal"))]

    # df['cross_and_mix_with_pred'] = [str(load_cross_and_mix(dataset_name, model_name, "_with_pred"))]
    # df['cross_and_mix_cot_pal_with_pred'] = [str(load_cross_and_mix(dataset_name, model_name, "_cot_pal_with_pred"))]
    # df['cross_and_mix_cot_p2c_with_pred'] = [str(load_cross_and_mix(dataset_name, model_name, "_cot_p2c_with_pred"))]
    # df['cross_and_mix_p2c_pal_with_pred'] = [str(load_cross_and_mix(dataset_name, model_name, "_p2c_pal_with_pred"))]

    df = df[['model_name', 'cot', 'pal', 'p2c', 'simple greedy', 'cross_and_mix']]

    # df = df[['model_name', 'cot', 'pal', 'p2c', 'simple greedy',
    #          'cross_and_mix', 'cross_and_mix_cot_pal', 'cross_and_mix_cot_p2c', 'cross_and_mix_p2c_pal',
    #         'cross_and_mix_with_pred', 'cross_and_mix_cot_pal_with_pred', 'cross_and_mix_cot_p2c_with_pred', 'cross_and_mix_p2c_pal_with_pred',]]

    return dataset_name, model_name, df


dfs = load_scores()
with open(f'scores.md', 'w') as f:
    for dataset_name in dfs:
        f.write(f'# {dataset_name} \n')
        f.write(dfs[dataset_name].to_markdown() + '\n\n\n')