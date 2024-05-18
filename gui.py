# Load libraries.
import gradio as gr
import requests

# Local Imports.
from listeners import *


# Define Gradio Interface
def gradio_interface():

    # Call root api to initialize chatbot agents.
    # api_url = "http://localhost:8000/"
    # response = requests.get(api_url)

    # if response.status_code == 200:
        with gr.Blocks(
            css='''
            #file{
                height: 70px;
            } 
            #tab{
                height: 500px;
                border-color: orange;
            } 
            #title{
                color: orange; 
                font-weight: bold; 
                font-size: x-large;
            }
            #query-input input {
                height: 100px;
                font-size: 18px;
            }
            #answer-output {
                font-size: 18px;
            }
            #upload-doc {
                background-color: orange;
                color: white;
            }
            #upload-doc:hover {
                background-color: white;
                color: orange;
            }
            ''', 
            title="LANGCHAIN Q/A AGENT",
            theme="") as demo:

            with gr.Row():
                with gr.Column(scale=0.50):
                    pass
                with gr.Column(scale=0.20):
                    title = gr.Markdown("LANGCHAIN Q/A AGENT", elem_id="title")
                with gr.Column(scale=0.30):
                    pass
                
            with gr.Tab("ChatBot", elem_id="tab"):
                with gr.Row():
                    pass
                with gr.Row():
                    with gr.Column(scale=0.20):
                        pass
                    with gr.Column(scale=0.60):
                        chatbot = gr.Chatbot(value=[], elem_id="chatbot", label="Q/A Agent (Search - Math)").style(height=650)
                    with gr.Column(scale=0.20):
                        pass
                with gr.Row():
                    with gr.Column(scale=0.20):
                        pass
                    with gr.Column(scale=0.60):
                        txt = gr.Textbox(
                            show_label=False,
                            placeholder="Enter text and press enter",
                        ).style(container=False) 
                    with gr.Column(scale=0.20):
                        pass

                txt.submit(process_query, [txt, chatbot], [txt, chatbot])
            with gr.Tab("Q/A PDF", elem_id="tab"):

                with gr.Row():
                    
                    with gr.Column(scale=0.6):
                        doc_query = gr.Textbox(
                            show_label=False,
                            placeholder="Ask Your Query Here and Press Enter", elem_id="query-input"
                        ).style(container=False) 
                    with gr.Column(scale=0.4):
                        pdf_uploader = gr.File(label="Upload PDF document", elem_id="file", show_label=False).style(height=100)


                with gr.Row():
                    with gr.Column(scale=0.6):
                        clear_button = gr.Button("Clear")
                    with gr.Column(scale=0.4):
                        doc_button = gr.Button("Upload PDF", elem_id="upload-doc")

                with gr.Row():
                    with gr.Column(scale=0.6):
                        doc_output = gr.Markdown(value="Answer", elem_id="answer-output")
                    with gr.Column(scale=0.4):
                        upload_status = gr.Markdown()
                    
                doc_button.click(uplaod_doc, inputs=pdf_uploader, outputs=upload_status)
                clear_button.click(clear_knowledge_base, inputs=[], outputs=[doc_query, doc_output, upload_status])

                doc_query.submit(process_doc_query, inputs=doc_query, outputs=[doc_output, upload_status])

        demo.queue(2)    
        demo.launch()


# Launch Gradio UI
gradio_interface()
