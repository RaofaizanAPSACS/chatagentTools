<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center" style="color: orange; font-weight: bold;">LANGCHAIN OPENAI CHATBOT AND PDF AGENT WITH INTERNET SEARCH AND WOLFRAMAPLHA TOOLS</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Langchain Chatbot Agent is an advanced conversational agent designed to provide comprehensive and accurate responses to user queries. Powered by OpenAI GPT-3.5, SerpAPI, and WolframAlpha, this project combines state-of-the-art language processing capabilities with powerful search and knowledge retrieval tools.


### Features

* Utilizes OpenAI GPT-3.5 to generate human-like responses, enabling natural and engaging conversations.
* Integrates SerpAPI to leverage the power of Google Search for reliable and up-to-date information retrieval.
* Harnesses the capabilities of WolframAlpha to access its vast knowledge base and deliver precise answers.
* Additionally, includes a PDF agent specialized in extracting and answering user queries related to PDF documents.



### Built With

* [Python3](https://www.python.org/)
* [LangChain](https://python.langchain.com/en/latest/index.html)
* [Gradio](https://gradio.app/)
* [FastAPI](https://fastapi.tiangolo.com/lo/)



<!-- GETTING STARTED -->
## Getting Started
Get up and running quickly with these simple steps!


## Installation

1. Clone the repository
   ```sh
   git clone https://github.com/RaofaizanAPSACS/langchain_q-a_agent
   ```
2. Install all required packages in the  `requirements.txt` file
   ```sh
   pip install -r requirements.txt
   ```
3. Create a .env file.

4. Get your [OPENAI_API_KEY](https://platform.openai.com/account/api-keys).

5. Go to wolfram alpha and sign up for a developer account [here](https://products.wolframalpha.com/api/)

6. Get your [serp api key](https://serpapi.com/).

7. Setup these keys as Environment Variables in `.env` file.



<!-- USAGE EXAMPLES -->
## Usage

Learn how to effectively use the Langchain Agents and its features with the following guidelines after doing Installation:

1. First move to project folder by using this command:
  ```sh
  cd langchain_q-a_agent
  ```
2. Start the FastAPI server using this command:
  ```sh
  uvicorn main:app --reload
  ```
3. Start the Gradio Interface:
  ```sh
  python gui.py
  ```
4. Go to the Gradio Localhost URL to open the Webpage.


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Helpful Resources:-

* [Langchain ReAct](https://python.langchain.com/en/latest/modules/agents/agents/examples/react.html)
* [Langchain ChatGPT Clone](https://python.langchain.com/en/latest/modules/agents/agent_executors/examples/chatgpt_clone.html)
* [Wolfram Alpha](https://python.langchain.com/en/latest/modules/agents/tools/examples/wolfram_alpha.html)
* [Serp API](https://python.langchain.com/en/latest/reference/modules/serpapi.html)
* [Gradio Controlling Layout](https://gradio.app/controlling-layout/)
* [Q/A with Docs](https://python.langchain.com/en/latest/use_cases/question_answering.html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>