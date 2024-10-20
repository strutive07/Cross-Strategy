from pathlib import Path
from typing import Literal

import yaml
from query_obj import BaseQueryObject, math_prompt


class PALQueryObject(BaseQueryObject):
    def __init__(self, dataset_type):
        self.dataset_type = dataset_type

    async def prepare_query(self, question: str, backbone: str, **kwargs):
        return get_pal_prompt(
            question, backbone=backbone, dataset_type=self.dataset_type
        )

    def query_error_msg(self, query_message):
        return False, None


def get_pal_prompt(
    question: str,
    backbone: str,
    dataset_type: Literal["gsm", "ocw", "math", "svamp"] = None,
):
    """
    This function is used to generate the PAL prompt.
    """
    if dataset_type not in "gsm ocw math svamp":
        raise ValueError(f"get_pal_prompt(): {dataset_type=} is not supported")

    from query_obj import get_user_assistant_messages

    if dataset_type == "gsm":
        if backbone == "gpt4" or backbone == "gpt4turbo":
            system_message = math_prompt.GPT4_PAL_SYSTEM
            user_message = math_prompt.GPT4_PAL_USER
            assistant_message = math_prompt.GPT4_PAL_ASSISTANT
            messages = get_user_assistant_messages(
                system_message, user_message, assistant_message
            )

            messages += [
                {
                    "role": "user",
                    "content": f"Question: {question}\n\n# solution in Python",
                }
            ]

        else:
            system_message = math_prompt.TURBO_PAL_SYSTEM
            user_message = math_prompt.TURBO_PAL_USER
            assistant_message = math_prompt.TURBO_PAL_ASSISTANT
            messages = get_user_assistant_messages(
                system_message, user_message, assistant_message
            )

            messages += [
                {
                    "role": "user",
                    "content": f"Answer the following question in Python: {question}",
                }
            ]
    elif dataset_type in ["ocw", "math", "svamp"]:
        # open ocw/MATH targeted CoT prompts
        THIS_PARENT = Path(__file__).parent.resolve()
        ymlf = THIS_PARENT / "ocw_MATH_prompts.yaml"
        prompt_d = yaml.full_load(open(ymlf))
        pmpt_d = prompt_d[f"{dataset_type}_pal"]
        system_message = pmpt_d["system"]
        user_msgs = pmpt_d["user"]

        # make it to a chat-history
        assistant_msgs = pmpt_d["assistant"]
        messages = [
            {"role": "system", "content": system_message},
        ]

        assert len(user_msgs) == len(
            assistant_msgs
        ), f"{len(user_msgs)=} should be equal to {len(assistant_msgs)=}"

        for u, a in zip(user_msgs, assistant_msgs):
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content": a})

        # add question of interest with the template
        user_attempt = pmpt_d["user_tmp"].replace("{QUESTION}", question)
        messages += [{"role": "user", "content": user_attempt}]

    else:
        raise ValueError(f"get_pal_prompt(): {dataset_type=} is not supported")

    return messages
