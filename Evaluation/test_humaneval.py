import json
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "Bin12345/AutoCoder"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, 
                                             device_map="auto")

HumanEval = load_dataset("evalplus/humanevalplus")

answers = []

for (index, data) in enumerate(HumanEval["test"]):
    print(f"Working on {index}\n")
    print(f"Original question:\n{data['prompt']}\n")
    question = data['prompt'].strip()
    content = f"""Write a solution to the following problem:
        ```python
        {question}
        ```"""
    messages=[
        { 'role': 'user', 'content': content}
    ]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, 
                                           return_tensors="pt").to(model.device)

    outputs = model.generate(inputs, 
                            max_new_tokens=1024, 
                            do_sample=False, 
                            temperature=0.0,
                            top_p=1.0, 
                            num_return_sequences=1, 
                            eos_token_id=tokenizer.eos_token_id)

    answer = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
    print(f"Answer:\n{answer}\n")
    json_data = {"task_id": f"HumanEval/{index}",
        "solution":f"{answer}" }

    # Save results to a JSON file
    with open('AutoCoder_HumanEval+.jsonl', 'a') as f:
        json.dump(json_data, f) 
        f.write('\n')

print("All data has been saved to AutoCoder_HumanEval+.jsonl")

