# AutoCoder

## News :fire: 

A new model [AutoCoder_QW_7B](https://huggingface.co/Bin12345/AutoCoder_QW_7B) is uploaded. In this model, We fixed the previous problem that the model will only start the code interpreter when you ask it to *verify* its code. 

The base model of AutoCode_QW_7B is [CodeQwen1.5-7b](https://huggingface.co/Qwen/CodeQwen1.5-7B-Chat).

## Introduction :mega:
We introduced a new model designed for the Code generation task. Its test accuracy on the HumanEval base dataset surpasses that of GPT-4 Turbo (April 2024). (**90.9% vs 90.2%**).

Additionally, compared to previous open-source models, AutoCoder offers a new feature: it can **automatically install the required packages** and attempt to run the code until it deems there are no issues, **whenever the user wishes to execute the code**.

* Difference between the code interpreter of AutoCoder and the GPT-4 Turbo:

Below are the video demos for the code interpreter comparison between GPT-4 Turbo and AutoCoder: 

GPT-4o can not access the external library.

[GPT-4o](https://github.com/bin123apple/AutoCoder/assets/99925255/be47b449-4e8a-4b77-981b-ec79b15970cc)

AutoCoder can automatically install the required packages. This feature expands the scope of code interpreter's application.

[AutoCoder](https://github.com/bin123apple/AutoCoder/assets/99925255/1893f904-c1f2-4f59-9ec5-45b69efcc26a)

* Difference between the code interpreter of AutoCoder and the current open-source code interpreter [OpenCodeInterpreter](https://opencodeinterpreter.github.io/):

The code interpreter of AutoCoder, like GPT-4 Turbo, is only called when the user has a need to verify the code, while OpenCodeInterpreter runs all generated python code.

## Model :gift:
The Model is avaliable on Huggingface:
 
[AutoCoder (33B)](https://huggingface.co/Bin12345/AutoCoder)
[AutoCoder-S (6.7B)](https://huggingface.co/Bin12345/AutoCoder_S_6.7B)

The base models of AutoCoder (33B) and AutoCoder-S (6.7B) are deepseeker-coder.

[AutoCoder_QW_7B](https://huggingface.co/Bin12345/AutoCoder_QW_7B)

The base model of AutoCoder_QW_7B is CodeQwen1.5-7b.

## Quick Start :rocket:
1. Create the conda env

```
conda create -n AutoCoder python=3.11
conda activate AutoCoder
pip install -r requirements.txt
```

2. Test on HumanEval **90.9% on base, 78.0% on base + extra**. (Skip to Step 5, if you don't want to test its performance on benchmarks)

```
cd Evaluation
python test_humaneval.py
```
You will receive a file named AutoCoder_HumanEval+.jsonl, which follows the EvalPlus format, after this step.

Then follow the testing framework of the [EvalPlus GitHub](https://github.com/evalplus/evalplus). You will see the results. 

**NOTE**: 
* Don't forget to use evalplus's `evalplus.sanitize` to post-process the code. 
* If you don't use the greedy method (for example set the `do_sample=True`) for the code generation. You will probably see the different results.

3. Test on MBPP **82.5% on base, 70.6% on base + extra**. (Skip to Step 5, if you don't want to test its performance on benchmarks)

```
python test_humaneval.py
```

Post-process to delete the nature language for testing
```
python postprocess_mbpp.py
```
Your will get a AutoCoder_Mbpp+-sanitized.jsonl file after this step, it extracted all the code blocks. 
Then, directly test it by using [EvalPlus GitHub](https://github.com/evalplus/evalplus) (You don't need to use to use evalplus's `evalplus.sanitize` to post-process the code this time).

4. Test on DS-1000. (Skip to Step 5, if you don't want to test its performance on benchmarks)

```
python test_ds1000.py
```

Your will get a jsonl file after this step, it extracted all the code blocks. 
Then, directly test it by using [DS-1000 GitHub](https://github.com/xlang-ai/DS-1000).

5. Web demo (Include code interpreter)

Install gradio related pakcages
```
cd /Web_demo
pip install -r requirements.txt
```

Run it:
```
python chatbot.py
```

## **NOTE** :warning:
* We suggest to set `do_sample = True` (default setting here) while using the code interpreter.

* It would be preferable to use Linux for deploying everything.

## Contact :email:
If you have any inquiries, please feel free to raise an issue or reach out to leib2765@gmail.com.

## Citation :book:
```
@misc{lei2024autocoder,
      title={AutoCoder: Enhancing Code Large Language Model with \textsc{AIEV-Instruct}}, 
      author={Bin Lei and Yuchen Li and Qiuwu Chen},
      year={2024},
      eprint={2405.14906},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```

## Acknowledgments :pray:
Thanks to Tianyu Zheng, the first author of the [OpenCodeInterpreter](https://opencodeinterpreter.github.io/), for guidance on some technical details.

