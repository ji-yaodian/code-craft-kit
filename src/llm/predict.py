import os
import sys
import time
import traceback

import openai


def get_llm_result(model, prompt, temperature=0, max_tokens=20, session_id="",
                   url='http://',
                   stop_list=['<|im_start|>', '<|im_end|>', "<|endoftext|>", "</s>", '<|end_of_text|>', '<|eot_id|>']):
    openai.api_key = "EMPTY"  # Not support yet

    openai.base_url = url

    start = time.perf_counter()
    completion = openai.completions.create(
        stop=stop_list,
        model=model, prompt=prompt, echo=False,
        temperature=temperature, max_tokens=max_tokens, timeout=120)
    res = completion.choices[0].text

    return res


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)
    url = 'http://10.16.16.139:25015/v1/'

    for input_file in os.listdir(input_dir):
        if not input_file.startswith('input'):
            continue
        if os.path.isfile(os.path.join(input_dir, input_file)):
            with open(os.path.join(input_dir, input_file), 'r') as f, \
                    open(os.path.join(output_dir, input_file.replace('input', 'output')), 'w') as fout:
                message = f.read()
                prompt = "<|begin_of_text|>" + f"<|start_header_id|>Human:<|end_header_id|>\n{message}\n<|eot_id|>\n"
                prompt += f"<|start_header_id|>Assistant:<|end_header_id|>\n"
                # print(input_file)
                try:
                    t0 = time.perf_counter()
                    res = get_llm_result(model='llama70b', prompt=prompt, temperature=0.75, max_tokens=1000, url=url)
                    t1 = time.perf_counter()
                    fout.write(res)
                    print(f"{input_file} cost time: {t1 - t0:.2f}s")
                except Exception as e:
                    print(e)
