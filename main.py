# Required Libraries.
import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"


from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.memory import  ConversationBufferWindowMemory
from langchain.utilities import SerpAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain import LLMChain, PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import get_openai_callback
from template import *

# Initializing the App.
app = FastAPI()

# Set knowledge base to None Initially.
knowledge_base = None

# load env variables.
load_dotenv()

history_str = ""

def direct(query):
    """
    This function will use the director gpt 3.5 to decide whether to use externals tools or not to answer 
    this query.
    """
    query = '"{}"'.format(query)
    yn = dllm([SystemMessage(content=directorSys), HumanMessage(content=query)]).content.lower()
    return 'yes' in yn


# Root controller.
@app.get("/")
def read_root():

    global tools, agent_chain, dllm, directorSys, chatgpt_chain, memory


    # set up GPT-3.5 director, which will decide whether to use tools or not.
    dllm = ChatOpenAI(temperature=0)
    directorSys = 'Does the following request require searching the internet, interacting with the filesystem, ' \
                'executing code, or doing math calculations?\nRespond only with yes or no.'

    # Initializeing WolframAlpha tool.
    wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid=os.getenv("WOLFRAM_ALPHA_APPID"))

    # Initializing SerpAPI tool for Google Search.
    search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

    # Creating tools list.
    tools = [
        Tool(
            name = "Current Search",
            func = search.run,
            description = "Useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
        ),
        Tool(
            name = "Math Operations",
            func=wolfram.run,
            description= "Useful for when you need to answer questions about mathematics."
        )
    ]


    # Create memory to maintain chat history during conversation.
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=10)

    # Initialize OpenAI LLM.
    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo")

    # Create a ReAct agent which uses all the above tools.
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    


    # Creating a ChatGPT tool.
    prompt = PromptTemplate(
        input_variables=["chat_history", "input"], 
        template=template
    )
    chatgpt_chain = LLMChain(
        llm=llm, 
        prompt=prompt, 
        verbose=True, 
    )

    return {"Status": "Agents Initialized"}

# Upload file controller.
@app.post("/uploadDoc")
def root(file_content: dict):

    content = file_content["file"]

    global knowledge_base

    # Check if content is not empty.
    if content != "":

        # Split the content into chunks.
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len
        )

        chunks = text_splitter.split_text(content)

        # Create Embeddings.
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        knowledge_base = FAISS.from_texts(chunks, embeddings)

    return {"file_name": len(chunks)}


# Upload file controller.
@app.post("/queryDoc")
def ask_query_doc(query_doc: dict):

    query = query_doc["query"]
    answer = ""
    
    if knowledge_base is not None:

        if query:

            docs = knowledge_base.similarity_search(query)
            
            llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
            chain = load_qa_chain(llm, chain_type="stuff")
            answer = chain.run(input_documents=docs, question=query)

    return {"Answer": answer}


# Controller
# Q/A chatbot with google search and wolfram alpha api.
@app.post("/querySearch")
def ask_query(request: dict):

    global history_str

    query = request["query"]
    answer = ""

    if query != "":

        with get_openai_callback() as cb:

            # First Save Human query in the history.
            history_str += "\nHuman: " + query

            # Decide which agent to use.
            if direct(query):

                # Feed the chatgpt last answer into this agent memory.
                messages = history_str.split("\n")
                if len(messages) > 2:
                    memory.chat_memory.add_ai_message(messages[-2])
                try:
                    answer = agent_chain.run(query)

                    # Save this agent's answer into a chatgpt history.
                    history_str += "\nAssistant: " + answer
                except Exception as e:
                    print('ERROR: ' + str(e))
            else:

                # Use chatgpt to answer query and maintian history.
                answer = chatgpt_chain.predict(input=query, chat_history=history_str)
                history_str += "\nAssistant: " + answer
            print(answer)

    return {"Answer": answer}



# Controller
# To clear the knowledge base of the uploaded PDF document.
@app.get("/removeDoc")
def ask_query():

    # Set knowledge base to None.
    knowledge_base = None
    
    return {"status": "Removed"}


