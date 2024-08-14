""" 
Sample Project Description:
project 1. 
I want to build a snake game, the snake will grow in length after it eat foods. the player use arrow to control its movement. 
the objective is not to crash to walls,otherwise the player will lose. press q to quit the game. press s to stop the game. 

project 2.
I want to build a calculator program , it will have add, minus, multipy, division, exponentiation, logarithms methods, and 
it also has a main method as the entry point to the program. 
The program has error handling mechanism by providing informative error messages. It also implemented unit tests in test folder for each of the 
methods to ensure the correctness of the calculatior's output.

"""
import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
import random
from llama_index.llms.fireworks import Fireworks
import os

os.environ["GROQ_API_KEY"] = "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"
# os.environ['FIREWORKS_API_KEY'] = '8nozAPErfL1PgACJgLIsUzKFPgGqabQGAPJ4z0VogUeiZhSb' # get a free key at https://fireworks.ai/api-keys
groq_hosted_llama = ChatGroq(
    model="llama-3.1-70b-versatile", #gemma2-9b-it
    # model="whisper-large-v3", #gemma2-9b-it
    # model="llama-3.1-8b-instant", #gemma2-9b-it
    temperature=1,
    max_tokens=1024,
    stop=None,
)

# firework_hosted_llama = Fireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct", temperature=0)# localllm = Ollama(model="codestral:latest")#llama3.1:8b 
llama8b_local = Ollama(model="llama3.1:8b")#llama3.1:8b 

llm = groq_hosted_llama
# Setup evn设置环境变量，
os.environ["OPENAI_API_BASE"] = 'http://localhost:3000/'
os.environ["OPENAI_MODEL_NAME"] ="llama-3.1-70b-versatile" # 'codestral:latest'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] ='ollama' #"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" #'ollama'

# Get user inputs
project_name = input("Please provide a project name, no space and length is within 10 characters.\n")
project_description = input("What is the program you would like to build? Please provide detailed description of the program and its requirements.")
code_language = input("what's the language of coding?")

# Define an Agent
senior_engineer_agent = Agent(
    llm=llm,
    role='Senior Software Engineer',
    goal='Create software as needed',
    backstory=dedent("""Instructions
                        You are a Senior Software Engineer at a leading tech think tank.
                        Your expertise in programming in {code_language}. and do your best to
                        produce perfect code, please use try catch for the main logic for any exceptions. """),
    allow_delegation=False,
    verbose=True
)

# Define an agent
qa_engineer_agent = Agent(
    llm=llm,
    role='Software Quality Control Engineer',
    goal='create prefect code, by analizing the code that is given for errors',
    backstory=dedent("""\
                        You are a software engineer that specializes in checking code
                        for errors. You have an eye for detail and a knack for finding
                        hidden bugs.
                        You check for missing imports, variable declarations, mismatched
                        brackets and syntax errors.
                        You also check for security vulnerabilities, and logic errors, and if it used try catch. """),
    allow_delegation=False,
    verbose=True
)

# Define an agent
chief_qa_engineer_agent = Agent(
    llm=llm,
    role='Chief Software Quality Control Engineer',
    goal='Ensure that the code does the job that it is supposed to do',
    backstory=dedent("""\
                        You feel that programmers always do only half of the job, so you are
                        super dedicate to make high quality code and if it used try catch."""),
    allow_delegation=True,
    verbose=True
)

# Define task
code_task = Task(
    llm=llm,
    description=dedent(f"""You will create a program using {code_language}, these are the instructions:
                
                            Instructions
                            ------------
                        {project_description}
                
                            Your Final answer must be the full {code_language} code, only the {code_language} code and nothing else and
                            and it should used try catch.
  			        """),
    expected_output="A complete {code_language} code implementing all specified mechanics, fully functional and commented.",
    agent=senior_engineer_agent
)

review_task = Task(
    llm=llm,
    description=dedent(f"""\
                            You are helping create a program using {code_language}, these are the instructions:
                
                            Instructions
                            ------------
                            {project_description}
                
                            Using the code you got, check for errors. Check for logic errors,
                            syntax errors, missing imports, variable declarations, mismatched brackets,
                            and security vulnerabilities.
                
                            Your Final answer must be the full {code_language} code, only the {code_language} code and nothing else
                            and it should used try catch.
  			        """),
    expected_output="An error-checked and corrected {code_language} code, ensuring no syntax, logical, or security flaws are present and it should used try catch.",
    agent=qa_engineer_agent
)

evaluate_task = Task(
    llm=llm,
    description=dedent(f"""\
                            You are helping create a program using {code_language}, these are the instructions:
                
                            Instructions
                            ------------
                            {project_description}
                
                            You will look over the code to insure that it is complete and
                            does the job that it is supposed to do.
                
                            Your Final answer must be the full {code_language} code, only the {code_language} code and nothing else
                            and it should used try catch.
			            """),
    expected_output="A finalized {code_language} code of the program that is reviewed for completeness, functionality, and optimization.",
    agent=chief_qa_engineer_agent
)

# Define the team
crew = Crew(
  agents=[senior_engineer_agent, qa_engineer_agent,chief_qa_engineer_agent],
  tasks=[code_task, review_task,evaluate_task],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# The team to start work
final_output_code = crew.kickoff()

# Print output
print("\n\n########################")
print("## Here is the final output code of result")
print("########################\n")
print("final code for the project:")
print(final_output_code)

#save it to local folder
# Create 'result' folder if it doesn't exist
result_folder = os.path.join(os.getcwd(), 'result')
os.makedirs(result_folder, exist_ok=True)

# Define the full path where the code file will be saved
filename = os.path.join(result_folder, f"{project_name}_{str(random.randint(1, 10))}.py")

# Write the code to the .py file in the 'result' folder
with open(filename, "w") as file:
    final_result=str.replace(str(final_output_code),"```","#```")
    # print("final"+final_result)
    file.write(final_result)