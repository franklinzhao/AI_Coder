###
# I want to build a snake game, the snake will grow in length after it eat foods. the player use arrow to control its movement. 
# the objective is not to crash to walls,otherwise the player will lose. press q to quit the game. press s to stop the game.
import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.llms import Ollama

os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama-3.1-70b-versatile", #gemma2-9b-it
    # model="whisper-large-v3", #gemma2-9b-it
    # model="llama-3.1-8b-instant", #gemma2-9b-it
    temperature=1,
    max_tokens=1024,
    stop=None,
)
local_llm = Ollama(model="codestral:latest")
# 设置环境变量，指定模型的基础URL、模型名称和API密钥
os.environ["OPENAI_API_BASE"] = 'http://localhost:3000/'
os.environ["OPENAI_MODEL_NAME"] ="llama-3.1-70b-versatile" # 'codestral:latest'  # Adjust based on available model
os.environ["OPENAI_API_KEY"] ='ollama' #"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" #'ollama'

# 获取用户输入的游戏类型和机制
game = input("What is software you would like to build? Please provide detailed description of the project and its requirements.\n")
code_language = input("what's the language of coding?")
# 定义一个高级软件工程师角色的Agent
senior_engineer_agent = Agent(
    llm=llm,
    role='Senior Software Engineer',
    goal='Create software as needed',
    backstory=dedent("""\Instructions
                        You are a Senior Software Engineer at a leading tech think tank.
                        Your expertise in programming in python. and do your best to
                        produce perfect code"""),
    allow_delegation=False,
    verbose=True
)

# 定义一个软件质量控制工程师角色的Agent
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
                        You also check for security vulnerabilities, and logic errors"""),
    allow_delegation=False,
    verbose=True
)

# 定义一个首席软件质量控制工程师角色的Agent
###本视频和代码由AI超元域频道原创 禁止盗搬 如有问题请联系我的徽信 stoeng
chief_qa_engineer_agent = Agent(
    llm=llm,
    role='Chief Software Quality Control Engineer',
    goal='Ensure that the code does the job that it is supposed to do',
    backstory=dedent("""\
                        You feel that programmers always do only half the job, so you are
                        super dedicate to make high quality code."""),
    allow_delegation=True,
    verbose=True
)

# # 为你的Agents创建任务
code_task = Task(
    llm=llm,
    description=dedent(f"""You will create a game using python, these are the instructions:
                
                            Instructions
                            ------------
                        {game}
                
                            Your Final answer must be the full python code, only the python code and nothing else.
  			        """),
    expected_output="A complete Python game code implementing all specified mechanics, fully functional and commented.",
    agent=senior_engineer_agent
)

review_task = Task(
    llm=llm,
    description=dedent(f"""\
                            You are helping create a game using python, these are the instructions:
                
                            Instructions
                            ------------
                            {game}
                
                            Using the code you got, check for errors. Check for logic errors,
                            syntax errors, missing imports, variable declarations, mismatched brackets,
                            and security vulnerabilities.
                
                            Your Final answer must be the full python code, only the python code and nothing else.
  			        """),
    expected_output="An error-checked and corrected Python game code, ensuring no syntax, logical, or security flaws are present.",
    agent=qa_engineer_agent
)

evaluate_task = Task(
    llm=llm,
    description=dedent(f"""\
                            You are helping create a game using python, these are the instructions:
                
                            Instructions
                            ------------
                            {game}
                
                            You will look over the code to insure that it is complete and
                            does the job that it is supposed to do.
                
                            Your Final answer must be the full python code, only the python code and nothing else.
			            """),
    expected_output="A finalized Python game code that is reviewed for completeness, functionality, and optimization.",
    agent=chief_qa_engineer_agent
)

# 用顺序流程实例化你的团队
###本视频和代码由AI超元域频道原创 禁止盗搬
crew = Crew(
  agents=[senior_engineer_agent, qa_engineer_agent,chief_qa_engineer_agent],
  tasks=[code_task, review_task,evaluate_task],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# 让你的团队开始工作！
game = crew.kickoff()

# 输出结果
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("final code for the game:")
print(game)