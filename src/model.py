import os, openai
from .utils import sanitize_one_line

class GenericModel:
    def __init__(self, model_name):
        self.model_name = model_name
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.mode = os.environ.get("KELP_SHELL")

    def query_model(self, prompt, sanitize=True):
        response = openai.Completion.create(
            engine=self.model_name,
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
            prompt=prompt
        )
        if sanitize:
            return sanitize_one_line(response.choices[0].text)
        else:
            return response.choices[0].text
    
    def correct_command(self, text):
        prompt = f"This command is wrong:\n{text}\n\nCorrect this command to its most probable and meaningful usage:\n$"
        return self.query_model(prompt)

    def explain_command(self, text):
        prompt = f"Explain this command:\n{text}\n\nExplanation:\n$"
        return self.query_model(prompt, sanitize=False)
    
    def check_dangerous_command(self, text):
        prompt = f"Check if command is dangerous:\n{text}\n\nDangerous:\n$"
        return self.query_model(prompt, sanitize=False)
    
    def get_command(self, text):
        # get number of words in the text
        num_words = len(text.split())
        if num_words > 30:
            raise ValueError("Text is too long")
        
        prompt = f"I want to do the following in a {self.mode} shell:\nInstruction:\n{text}\n\nGive me the command for that:\n$"
        return self.query_model(prompt)
        
    
class GPT3Model(GenericModel):
    # GPT-3 Davinci
    # Deprecated, use GPT35Model instead

    def __init__(self):
        super().__init__(model_name="text-davinci-003")

class GPT35Model(GenericModel):
    # GPT-3.5 Turbo
    # This is the model used in the demo

    def __init__(self):
        super().__init__(model_name="gpt-3.5-turbo-instruct")

if __name__ == "__main__":
    model = GPT35Model()
    print(model.correct_command("gi t pulll orign mian"))
    print(model.explain_command("ls -l"))
    print(model.check_dangerous_command("rm -rf /"))
    print(model.get_command("list all the files in the current directory and show their permissions, then output the result to a file called 'permissions.txt'"))
    print(model.get_command("create an empty react template app in typescript"))