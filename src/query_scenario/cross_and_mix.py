# start from processed_indiv

import asyncio
from typing import Dict, List

import pandas as pd
from query_obj import CrossAndMixQueryObject


def solutions_d_from_row(row: Dict = None, with_pred=False) -> Dict[str, List[str]]:
    sln_d = dict()
    for method in "cot pal p2c".split():
        sln_d[method] = row[f"{method}_solutions"]

        if with_pred and method in ["pal", "p2c"]:
            method_pred = row[f"{method}_preds"][0]
            sln_d[method][0] += f"\n\nFinal Answer: {method_pred}"

    return sln_d


def unwrap_and_listify(d: Dict[str, List[str]] = None) -> List[Dict[str, str]]:
    unwrapped = pd.DataFrame(d).to_dict(orient="records")
    return unwrapped


async def cross_and_mix_query(
    # indiv_records_path:Union[str, Path]="some.jsonl",
    row: Dict = None,
    temperature: float = 0.0,
    n: int = 1,
    seed: int = 777,
    backbone: str = "",
    prompt_yml_file: str = "cross_and_mix_prompts.yaml",
    with_pred=False
    # dataset_type: Literal["gsm", "ocw", "math"] = "",
):
    """
    process row and query selection (cross-and-mix)

    assume this function gets only rows that requires selection
    """
    dataset_type = row["dataset_type"]
    assert dataset_type in "gsm ocw math svamp".split(), f"check {dataset_type=}"
    assert backbone, f"{backbone=} must be passed!"
    if '_with_pred' in prompt_yml_file:
        assert with_pred, "check with_pred param"

    # init
    query_obj = CrossAndMixQueryObject(
        dataset_type=dataset_type,
        prompt_yml_file=prompt_yml_file,
    )

    # placeholders
    return_data = {}
    jobs = []

    question = row["question"]
    cot_pal_p2c_sln_d = solutions_d_from_row(row=row, with_pred=with_pred)
    cot_pal_p2c_sln_d = unwrap_and_listify(d=cot_pal_p2c_sln_d)

    max_tokens = 2048

    for c_p_p2_sln in cot_pal_p2c_sln_d:
        query_params = {
            "question": question,
            "cot_pal_p2c_sln_d": c_p_p2_sln,
            "temperature": temperature,
            "backbone": backbone,
            "n": n,
            "seed": seed,
            "max_tokens": max_tokens
        }

        jobs.append(query_obj.async_query(**query_params))

    for contents, query_message, resp, meta in await asyncio.gather(*jobs):
        meta["gt_answer"] = row["gt_answer"]
        return_data[meta["method_obj"]] = {
            "contents": contents,  # already listified
            "query_message": query_message,
            "resp": resp,
            "meta": meta,
        }
    return return_data
