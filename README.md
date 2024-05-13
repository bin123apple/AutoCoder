# AutoCoder

## Introduction
We introduced a new model designed for the Code generation task. Its test accuracy on the HumanEval base dataset surpasses that of GPT-4 Turbo (April 2024). (90.9% vs 90.2%).

Additionally, compared to previous open-source models, AutoCoder offers a new feature: it can **automatically install the required packages** and attempt to run the code until it deems there are no issues, **whenever the user wishes to execute the code**.

Here are the video demos for the code interpreter comparision between GPT-4 Turbo and AutoCoder: 

[GPT-4 Turbo](https://github.com/bin123apple/AutoCoder/assets/99925255/b4079c2c-504d-4e56-ad94-c3a18f4360ec)

[AutoCoder](https://github.com/bin123apple/AutoCoder/assets/99925255/1893f904-c1f2-4f59-9ec5-45b69efcc26a)

## Model
The Model is avaliable on Huggingface: [Fortran2Cpp](https://huggingface.co/Bin12345/F2C-Translator)

### Quick Start
1. Create the conda env

```
conda create -n AutoCoder python=3.11
conda activate AutoCoder
pip install -r requirements.txt
```

2. Test on HumanEval 

```
cd Evaluation
python test_humaneval.py
```
You will receive a file named AutoCoder_HumanEval+.jsonl, which follows the EvalPlus format, after this step.

Then follow the testing framework of the [EvalPlus GitHub](https://github.com/evalplus/evalplus). You will see the results (90.9% on base, 78.0% on base + extra). 

NOTE: 
* Don't forget to use evalplus's `evalplus.sanitize` to post-process the code. 
* If you don't use the greedy method (for example set the `do_sample=True`) for the code generation. You will probably see the different results.

3. Enter into Evaluation folder

```
cd Evaluation
```

## Contact 
If you have any inquiries, please feel free to raise an issue or reach out to leib2765@gmail.com.

## Citation
We will complete the technical introduction paper soon.

## Acknowledgments
Thanks to Tianyu Zheng, the first author of the [OpenCodeInterpreter](https://opencodeinterpreter.github.io/), for guidance on some technical details.

