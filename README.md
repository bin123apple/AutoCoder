# AutoCoder

## Introduction
We introduced a new model designed for the Code generation task. Its test accuracy on the HumanEval base dataset surpasses that of GPT-4 Turbo (April 2024). (90.9% vs 90.2%).

Additionally, compared to previous open-source models, AutoCoder offers a new feature: it can **automatically install the required packages** and attempt to run the code until it deems there are no issues, **whenever the user wishes to execute the code**.

Here are the video demos:

[GPT-4 Turbo](AutoCoder/video_demo/gpt-4_turbo_result.mp4)

## Model
The Model is avaliable on Huggingface: [Fortran2Cpp](https://huggingface.co/Bin12345/F2C-Translator)


## Evaluation

 

### Reproduce Steps
1. Enter into Evaluation folder

```
cd Evaluation
```

2. Generate the results. Go the script `text_generation_pipline.py`. Add your own huggingface token to line 16. Modify the path where you want to store your results in line 55. Then select the model that you want to test between line 8 and line 13.

Run:
```
python text_generation_pipline.py
```

This will generate the results and compress each result to one line for the further CodeBLEU Score test.

3. Test CodeBLEU Score by using the following command

```
cd CodeBLEU
python calc_code_bleu.py --refs Fortran2Cpp/Evaluation/Groundtruth_C++.txt --hyp <path/to/your/results/txt/file> --lang cpp --params 0.25,0.25,0.25,0.25
```

## Inference and Demo
The demo code is modified from [OpenCodeInterpreter](https://github.com/OpenCodeInterpreter/OpenCodeInterpreter/tree/main/demo). Appreciate for their great project!

1. Create conda and install packages
```
cd Web_demo
conda create -n demo python=3.10
conda activate demo
pip install -r requirements.txt
```

2.  Start the demo
```
python chatbot.py
```

**NOTE:** This demo will not use the interpreter function. This feature is a potential extension for this work.

## Hardware requirements

We used 6 A100 GPUs with 80GB memory for the training.  (Use Lora)

We used 2 A100 GPUs with 80GB memory for the inference. 

## Contact 
If you have any inquiries, please feel free to raise an issue or reach out to leib2765@gmail.com.

## Citation
We will complete the technical introduction paper before mid-May.
