import ast
import gradio as gr
import os
import re
import json
import logging
import subprocess

import torch
import atexit
from datetime import datetime

from threading import Thread
from typing import Optional
from transformers import TextIteratorStreamer
from functools import partial
from huggingface_hub import CommitScheduler
from uuid import uuid4
from pathlib import Path

from code_interpreter.JupyterClient import JupyterNotebook

MAX_INPUT_TOKEN_LENGTH = int(os.getenv("MAX_INPUT_TOKEN_LENGTH", "4096"))

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

'''
This demo code is modified from https://github.com/OpenCodeInterpreter/OpenCodeInterpreter/tree/main/demo. 
'''

from code_interpreter.AutoCoderInterpreter import AutoCoderInterpreter

JSON_DATASET_DIR = Path("json_dataset")
JSON_DATASET_DIR.mkdir(parents=True, exist_ok=True)

scheduler = CommitScheduler(
    repo_id="AutoCoder_user_data",
    repo_type="dataset",
    folder_path=JSON_DATASET_DIR,
    path_in_repo="data",
    private=True
)

logging.basicConfig(level=logging.INFO)

class StreamingAutoCodeInterpreter(AutoCoderInterpreter):
    streamer: Optional[TextIteratorStreamer] = None

    # overwirte generate function
    @torch.inference_mode()
    def generate(
        self,
        inputs,
        max_new_tokens = 1024,
        do_sample: bool = True,
        top_p: float = 0.95,
        top_k: int = 50,
    ) -> str:

        self.streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, Timeout=5
        )
        logging.info(f"inputs:\n{inputs}")
        inputs = inputs.to(self.model.device)

        kwargs = dict(
            input_ids = inputs,
            streamer=self.streamer,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            top_k = top_k,
            top_p = top_p,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        logging.info(f"kwargs:\n{kwargs}")
        
        thread = Thread(target=self.model.generate, kwargs=kwargs)
        thread.start()

        return ""

def save_json(dialog, mode, json_file_path, dialog_id) -> None:
    with scheduler.lock:
        with json_file_path.open("a") as f:
            json.dump({"id": dialog_id, "dialog": dialog, "mode": mode, "datetime": datetime.now().isoformat()}, f, ensure_ascii=False)
            f.write("\n")

def convert_history(gradio_history: list[list], interpreter_history: list[dict]):
    interpreter_history = [interpreter_history[0]] if interpreter_history and interpreter_history[0]["role"] == "system" else []
    if not gradio_history:
        return interpreter_history
    for item in gradio_history:
        if item[0] is not None:
            interpreter_history.append({"role": "user", "content": item[0]})
        if item[1] is not None:
            interpreter_history.append({"role": "assistant", "content": item[1]})
    return interpreter_history

def update_uuid(dialog_info):
    new_uuid = str(uuid4())
    logging.info(f"allocating new uuid {new_uuid} for conversation...")
    return [new_uuid, dialog_info[1]]

def is_valid_python_code(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


class InputFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found_input = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'input':
            self.found_input = True
        self.generic_visit(node)

def has_input_function_calls(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    visitor = InputFunctionVisitor()
    visitor.visit(tree)
    return visitor.found_input

def gradio_launch(model_path: str, MAX_TRY: int = 3):
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(height=600, label="AutoCoder", avatar_images=["assets/user.pic.jpg", "assets/assistant.pic.jpg"], show_copy_button=True)
        with gr.Group():
            with gr.Row():
                msg = gr.Textbox(
                    container=False,
                    show_label=False,
                    label="Message",
                    placeholder="Type a message...",
                    scale=7,
                    autofocus=True
                )
                sub = gr.Button(
                    "Submit",
                    variant="primary",
                    scale=1,
                    min_width=150
                )
                # stop = gr.Button(
                #     "Stop",
                #     variant="stop",
                #     visible=False,
                #     scale=1,
                #     min_width=150
                # )

        with gr.Row():
            # retry = gr.Button("🔄  Retry", variant="secondary")
            # undo = gr.Button("↩️ Undo", variant="secondary")
            clear = gr.Button("🗑️  Clear", variant="secondary")

        session_state = gr.State([])
        dialog_info = gr.State(["", 0])
        demo.load(update_uuid, dialog_info, dialog_info)

        def bot(user_message, history, dialog_info, 
                interpreter, image_name, container_name, 
                dockerfile_name, sandbox_path, volume_mount):
            
            ## Initialize everything
            
            # log user input message
            logging.info(f"user message:\n {user_message}")
            
            # interpreter.dialog is inialize as []
            interpreter.dialog = convert_history(gradio_history=history, interpreter_history=interpreter.dialog)
            
            # Add user message to the history [user_msg, assistant_msg]
            history.append([user_message, None])
            
            # Add user message to the dialogue
            interpreter.dialog.append({"role": "user", "content": user_message})

            # Initialize the HAS_CODE = False
            HAS_CODE = False  
            
            ## Generate the assistant response
            
            # Apply chat template
            inputs = interpreter.dialog_to_prompt(dialog=interpreter.dialog)

            # Generate the assistant response
            _ = interpreter.generate(inputs)
            history[-1][1] = ""
            generated_text = ""
            code_blocks = ""
            code_block = ""
            for character in interpreter.streamer:
                history[-1][1] += character
                history[-1][1] = history[-1][1].replace("<|EOT|>","").replace("<API_RUN_START>","").replace("<API_RUN_STOP>","")
                generated_text += character
                yield history, history, dialog_info
            print("generated_text",generated_text)
            
            # Add the assistant response to the dialogue
            interpreter.dialog.append(
                {
                    "role": "assistant",
                    "content": generated_text.replace("<unk>_", "")
                    .replace("<unk>", "")
                    .replace("<|EOT|>", ""),
                }
            )
            
            HAS_CODE, generated_code_block = interpreter.extract_code_blocks(
                generated_text
            )

            logging.info(f"saving current dialog to file {dialog_info[0]}.json...")
            logging.info(f"current dialog: {interpreter.dialog}")
            save_json(interpreter.dialog, mode="openci_only", json_file_path=JSON_DATASET_DIR/f"{dialog_info[0]}.json", dialog_id=dialog_info[0])

            # uncomment this line for the no interpreter demo
            # HAS_CODE = False
            
            # Set up docker related path
            attempt = 1
            
            print(f"HAS_Code:{HAS_CODE}")
            # Enter into code interpreter and run the code
            while HAS_CODE:
                if attempt > MAX_TRY:
                    break
                
                # if no code then doesn't have to execute it
                generated_text = "" # clear generated text

                yield history, history, dialog_info

                # preprocess for the each kinds of generated code
                for lang, code in generated_code_block.items():
                    processed_code = code.replace("<unk>_", "").replace("<unk>", "")
                    generated_code_block[lang] = processed_code

                # exclude languages that do not require code execution
                generated_code_block = {lang: code for lang, code in generated_code_block.items() if code.strip()}
                print("generated_code_block",generated_code_block)
                
                # Check if need to install the external library
                matches_with_pip = []
                if "sh" in generated_code_block:
                    matches_with_pip.append(generated_code_block['sh'])
                    logging.info("We need to install new packages...")
                    
                # create the sandbox enviroment and run each kinds of codes
                has_problem, code_blocks_output = interpreter.execute_code_and_return_output(generated_code_block, 
                                                                                matches_with_pip, 
                                                                                image_name, container_name, 
                                                                                dockerfile_name, sandbox_path)
                print("code_blocks_output",code_blocks_output)

                # postprocess
                result_string = code_blocks_output['python'].rstrip()
                print("result_string",result_string)
                history.append([result_string, ""])

                interpreter.dialog.append({"role": "user", "content": result_string})

                yield history, history, dialog_info
                
                
                ## Generate the assistant response
                inputs = interpreter.dialog_to_prompt(dialog=interpreter.dialog)

                logging.info(f"generating answer for dialog {dialog_info[0]}")
                _ = interpreter.generate(inputs)
                for character in interpreter.streamer:
                    history[-1][1] += character
                    history[-1][1] = history[-1][1].replace("<|EOT|>","").replace("<API_RUN_START>","").replace("<API_RUN_STOP>","")
                    generated_text += character
                    yield history, history, dialog_info
                logging.info(f"finish generating answer for dialog {dialog_info[0]}")

                interpreter.dialog.append(
                    {
                        "role": "assistant", 
                        "content": generated_text.replace("<unk>_", "")
                        .replace("<unk>", "")
                        .replace("<|EOT|>", ""),
                    }
                )
                
                HAS_CODE, generated_code_block = interpreter.extract_code_blocks(
                    generated_text
                )


                # Try more times
                attempt += 1

                logging.info(f"saving current dialog to file {dialog_info[0]}.json...")
                logging.info(f"current dialog: {interpreter.dialog}")
                save_json(interpreter.dialog, mode="openci_only", json_file_path=JSON_DATASET_DIR/f"{dialog_info[0]}.json", dialog_id=dialog_info[0])

                if generated_text.endswith("<|EOT|>"):
                    continue

            return history, history, dialog_info


        def reset_textbox():
            return gr.update(value="")

        def clean_docker_container(container_name):
            try:
                subprocess.run(["docker", "rm", "-f", container_name], check=True)
                print(f"Container named {container_name} has been removed.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while removing the container {container_name}: {e}")
                
        def clear_history(history, dialog_info, interpreter, container_name):
            interpreter.dialog = []
            clean_docker_container(container_name)
            return [], [], update_uuid(dialog_info)
        
        def on_exit():
            clean_docker_container(container_name)

        atexit.register(on_exit)
        interpreter = StreamingAutoCodeInterpreter(model_path=model_path)
        
        index = 0
        image_name = f"python-sandbox_{index}"
        container_name = f"container_python_{index}"
        dockerfile_name = "Dockerfile.python"
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        main_path = os.path.join(current_directory, "sandbox")
        sandbox_path = f"{main_path}/python_{index}"
        volume_mount = f"{sandbox_path}:/app"

        # Creat docker image 
        check_command = ["docker", "images", "-q", image_name]
        image_exists = subprocess.run(check_command, capture_output=True, text=True).stdout.strip()
        if not image_exists:
            dockerfile_path = os.path.join(sandbox_path, dockerfile_name)
            # lang_sandbox_path = f"{sandbox_path}/{lang}/"
            lang_sandbox_path = f"{sandbox_path}"
            build_command = ["docker", "build", "-t", image_name, "-f", dockerfile_path, lang_sandbox_path]
            build_result = subprocess.run(build_command, capture_output=True, text=True)
            if build_result.returncode != 0:
                print(f"Failed to build image {image_name}: {build_result.stderr}")
                # code_blocks_output[lang] = f"Failed to build image {image_name}: {build_result.stderr}"
        
        # Keeping the docker backend running
        subprocess.run(["docker", "run", "-d", "-v", 
                        volume_mount, "--name", f"{container_name}", 
                        image_name, "tail", "-f", "/dev/null"], check=True)
        
        sub.click(partial(bot, interpreter=interpreter, image_name = image_name, 
                          container_name = container_name, dockerfile_name = dockerfile_name,
                          sandbox_path = sandbox_path, volume_mount = volume_mount), 
                  [msg, session_state, dialog_info], 
                  [chatbot, session_state, dialog_info])
        sub.click(reset_textbox, [], [msg])

        clear.click(partial(clear_history, interpreter=interpreter, container_name = container_name), [session_state, dialog_info], [chatbot, session_state, dialog_info], queue=False)

    demo.queue(max_size=20)
    demo.launch(share=True, server_port = 7000)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=False,
        help="Path to the Model.",
        default="Bin12345/AutoCoder",
    )
    args = parser.parse_args()

    gradio_launch(model_path=args.path)
