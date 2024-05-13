import os
import sys
import re
import logging
import subprocess

prj_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(prj_root_path)


from utils.const import *

class BaseCodeInterpreter:
    def __init__(self):
        self.dialog = [
            {
                "role": "system",
                "content": CODE_INTERPRETER_SYSTEM_PROMPT,
            },
        ]

    @staticmethod
    def extract_code_blocks(text: str):
        pattern = r"```(?:python\n)?(.*?)```"  # Match optional 'python\n' but don't capture it
        code_blocks = re.findall(pattern, text, re.DOTALL)
        return [block.strip() for block in code_blocks]

    # def execute_code_and_return_output(self, code_str: str, nb):
    #     _, _ = nb.add_and_run(GUARD_CODE)
    #     outputs, error_flag = nb.add_and_run(code_str)
    #     return outputs, error_flag

    # def execute_code_and_return_output(self, generated_code_block) -> str:
    #     code_blocks_output= {}
    #     sandbox_path = "/home/uconn/BinLei/Data_engine/NLP_Task/multi_codes_demo/sandbox"
    #     file_map = {"python": "script.py", "cpp": "script.cpp", "fortran": "script.f90"}
    #     image_map = {"python": "python-sandbox", "cpp": "cpp-sandbox", "fortran": "fortran-sandbox"}
    #     dockerfile_map = {"python": "python/Dockerfile.python", "cpp": "cpp/Dockerfile.cpp", "fortran": "fortran/Dockerfile.fortran"}
    #     for lang, code in generated_code_block.items():
            
    #         file_name = file_map[lang]
    #         image_name = image_map[lang]
            
    #         print(f"Writing the script for {lang}...")
    #         file_path = f"{sandbox_path}/{lang}/{file_name}"
    #         with open(file_path, 'w') as file:
    #             file.write(code)
            
    #         # check and build the image
    #         print(f"Checking if the image for {lang}... exist")
    #         image_name = image_map[lang]
    #         check_command = ["docker", "images", "-q", image_name]
    #         image_exists = subprocess.run(check_command, capture_output=True, text=True).stdout.strip()
            
    #         if not image_exists:
    #             print(f"Creating the image for {lang}...")
    #             dockerfile_path = os.path.join(sandbox_path, dockerfile_map[lang])
    #             lang_sandbox_path = f"{sandbox_path}/{lang}/"
    #             build_command = ["docker", "build", "-t", image_name, "-f", dockerfile_path, lang_sandbox_path]
    #             build_result = subprocess.run(build_command, capture_output=True, text=True)
    #             if build_result.returncode != 0:
    #                 print(f"Failed to build image {image_name}: {build_result.stderr}")
    #                 code_blocks_output[lang] = f"Failed to build image {image_name}: {build_result.stderr}"
    #                 continue
            
            
    #         print(f"Running the script for {lang} in the sandbox...")
    #         script_path = f"{sandbox_path}/{lang}/compile_run.sh"
    #         chmod_command = ["chmod", "+x", script_path]
    #         chmod_result = subprocess.run(chmod_command, capture_output=True, text=True)
    #         volume_mount = f"{sandbox_path}/{lang}:/app"
    #         command = ["docker", "run", "--rm", "-v", volume_mount, image_name]
    #         # command = ["docker", "run", "--rm", image_name]
    #         result = subprocess.run(command, capture_output=True, text=True)
            
    #         if result.returncode == 0: 
    #             code_blocks_output[lang] = result.stdout 
    #         else: 
    #             code_blocks_output[lang] = result.stderr
    #     return code_blocks_output
    
    def execute_code_and_return_output(self, generated_code_block,matches_with_pip, 
                                    image_name, container_name, 
                                    dockerfile_name, sandbox_path) -> str:
        
        # Initialize the file/image/dockerfile information for each langauges
        code_blocks_output= {}
        # sandbox_path = "/home/uconn/BinLei/Data_engine/NLP_Task/multi_codes_demo/sandbox"
        file_map = {"python": "script.py", 
                    "cpp": "script.cpp", 
                    "fortran": "script.f90"}
        # image_map = {"python": "python-sandbox", 
        #              "cpp": "cpp-sandbox", 
        #              "fortran": "fortran-sandbox"}
        # dockerfile_map = {"python": "python/Dockerfile.python", 
        #                   "cpp": "cpp/Dockerfile.cpp", 
        #                   "fortran": "fortran/Dockerfile.fortran"}
        image_map = {"python": f"{image_name}", 
                    "cpp": "cpp-sandbox", 
                    "fortran": "fortran-sandbox"}
        dockerfile_map = {"python": f"{dockerfile_name}", 
                        "cpp": "cpp/Dockerfile.cpp", 
                        "fortran": "fortran/Dockerfile.fortran"}
        has_problem = True
        for lang, code in generated_code_block.items():
            if lang == "sh":
                lang = "python"
            # write the script into the corresponsing file
            file_name = file_map[lang]
            image_name = image_map[lang]
            # file_path = f"{sandbox_path}/{lang}/{file_name}"
            file_path = f"{sandbox_path}/{file_name}"
            with open(file_path, 'w') as file:
                file.write(code)
            
            # check and build the image
            image_name = image_map[lang]
            check_command = ["docker", "images", "-q", image_name]
            image_exists = subprocess.run(check_command, capture_output=True, text=True).stdout.strip()
            
            if not image_exists:
                dockerfile_path = os.path.join(sandbox_path, dockerfile_map[lang])
                # lang_sandbox_path = f"{sandbox_path}/{lang}/"
                lang_sandbox_path = f"{sandbox_path}"
                build_command = ["docker", "build", "-t", image_name, "-f", dockerfile_path, lang_sandbox_path]
                build_result = subprocess.run(build_command, capture_output=True, text=True)
                if build_result.returncode != 0:
                    print(f"Failed to build image {image_name}: {build_result.stderr}")
                    code_blocks_output[lang] = f"Failed to build image {image_name}: {build_result.stderr}"
                    continue
            
            # give docker the access to run the comile_run file 
            # script_path = f"{sandbox_path}/{lang}/compile_run.sh"
            script_path = f"{sandbox_path}/compile_run.sh"
            chmod_command = ["chmod", "+x", script_path]
            chmod_result = subprocess.run(chmod_command, capture_output=True, text=True)
            # volume_mount = f"{sandbox_path}/{lang}:/app"
            volume_mount = f"{sandbox_path}:/app"
            
            # install external library for python if there are related commonds
            pip_command = None
            print("matches_with_pip",matches_with_pip)
            if lang == "python" and matches_with_pip: 
                pip_commands = []
                for match in matches_with_pip:
                    pattern = r'^pip install.*'
                    matches_pip = re.findall(pattern, match, re.MULTILINE)
                    print("matches_pip", matches_pip)
                    for match_pip in matches_pip:
                        if match_pip:
                            pip_commands.append(match_pip.replace('\n', ' ').strip())
                print(f"pip_command:{pip_command}")
                pip_command = " && ".join(pip_commands)
                print(f"pip_command:{pip_command}")
                if pip_command:
                    # command = ["docker", "exec", "container_python", "sh", "-c", f"{pip_command}"]
                    command = ["docker", "exec", f"{container_name}", "sh", "-c", f"{pip_command}"]
                    # print(f"command:{command}")
                    try:
                        logging.info("Start to install related packages...")
                        pip_result = subprocess.run(command, check=True, 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE, 
                                                    text=True)   
                    except subprocess.CalledProcessError as e:
                        pip_result = e
                    # command = ["docker", "exec", "container_python", "python", "/app/script.py"]
                    command = ["docker", "exec", f"{container_name}", "python", "/app/script.py"]
            
            # if there is no external library for python, execute the code directly
            else:    
                # command = ["docker", "exec", "container_python", "python", "/app/script.py"]
                command = ["docker", "exec", f"{container_name}", "python", "/app/script.py"]
            # result = subprocess.run(command, capture_output=True, text=True)
            try:
                logging.info("Start to run the code...")
                result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            except subprocess.TimeoutExpired:
                code_blocks_output[lang] = "Command execution timed out. This is probably because the function needs to run continuously."
                continue
            # record all the information into the code_blocks_output
            if result.stdout == "":
                result.stdout = "None"
            if result.stderr == "":
                has_problem = False
                result.stderr = "None"
            if pip_command:
                code_blocks_output[lang] = f"pip_result.stdout: \n{pip_result.stdout}\n pip_result.stderr: \n{pip_result.stderr}\n result.stdout:\n{result.stdout}\nresult.stderr:\n{result.stderr}"
            else:
                code_blocks_output[lang] = f"result.stdout:\n{result.stdout}\nresult.stderr:\n{result.stderr}"
        return has_problem, code_blocks_output