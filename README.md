# AutoCoder

## Introduction
We introduced a new model designed for the Code generation task. Its test accuracy on the HumanEval base dataset surpasses that of GPT-4 Turbo (April 2024). (90.9% vs 90.2%).

Additionally, compared to previous open-source models, AutoCoder offers a new feature: it can **automatically install the required packages** and attempt to run the code until it deems there are no issues, **whenever the user wishes to execute the code**.

* Difference between the code interpreter of AutoCoder and the GPT-4 Turbo:

Below are the video demos for the code interpreter comparision between GPT-4 Turbo and AutoCoder: 

GPT-4 Turbo can not access the external library.
[GPT-4 Turbo](https://github.com/bin123apple/AutoCoder/assets/99925255/b4079c2c-504d-4e56-ad94-c3a18f4360ec)

AutoCoder can automatically install the required packages. This feature expands the scope of code interpreter's application.
[AutoCoder](https://github.com/bin123apple/AutoCoder/assets/99925255/1893f904-c1f2-4f59-9ec5-45b69efcc26a)

* Difference between the code interpreter of AutoCoder and the current open-source code interpreter [OpenCodeInterpreter](https://opencodeinterpreter.github.io/):

The code interpreter of AutoCoder, like GPT-4 Turbo, is only called when the user has a need to verify the code, while OpenCodeInterpreter runs all generated python code.

## Model
The Model is avaliable on Huggingface: [AutoCoder](Bin12345/AutoCoder)

The base model is deepseeker 33B.

### Quick Start
1. Create the conda env

```
conda create -n AutoCoder python=3.11
conda activate AutoCoder
pip install -r requirements.txt
```

2. Test on HumanEval (90.9% on base, 78.0% on base + extra). 

```
cd Evaluation
python test_humaneval.py
```
You will receive a file named AutoCoder_HumanEval+.jsonl, which follows the EvalPlus format, after this step.

Then follow the testing framework of the [EvalPlus GitHub](https://github.com/evalplus/evalplus). You will see the results. 

NOTE: 
* Don't forget to use evalplus's `evalplus.sanitize` to post-process the code. 
* If you don't use the greedy method (for example set the `do_sample=True`) for the code generation. You will probably see the different results.

3. Test on MBPP (82.5% on base, 70.6% on base + extra). 

```
python test_humaneval.py
```

Post-process to delete the nature language for testing
```
python postprocess_mbpp.py
```
Your will get a AutoCoder_Mbpp+-sanitized.jsonl file after this step, it extracted all the code blocks. 
Then, directly test it by using [EvalPlus GitHub](https://github.com/evalplus/evalplus) (You don't need to use to use evalplus's `evalplus.sanitize` to post-process the code this time).

4. Web demo (Include code interpreter)

Install gradio related pakcages
```
cd /Web_demo
pip install -r requirements.txt
```

Run it:
```
python chatbot.py
```

NOTE:
* This demo is NOT totally finished yet, there are still some bugs. One know bug is that the docker container will not be removed if use `ctrl + c` to kill the process. I will fix it soon. For now, you can 
click `Clear` bottom to remove the docker container for now. 

* Currently the model will only start the code interpreter if you ask it to **verify** its code. I am still finetuning it on a instructed dataset, which will give it the ability to enable the code interpreter upon a user request to **run** code. I will update the model when it is finished.

* We suggest to set `do_sample = True` (default setting here) while using the code interpreter.


## Contact 
If you have any inquiries, please feel free to raise an issue or reach out to leib2765@gmail.com.

## Citation
We will complete the technical introduction paper soon.

## Acknowledgments
Thanks to Tianyu Zheng, the first author of the [OpenCodeInterpreter](https://opencodeinterpreter.github.io/), for guidance on some technical details.

