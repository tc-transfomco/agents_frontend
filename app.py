import gradio
import requests
from typing import Optional, Dict, Any, List, Tuple
from dotenv import load_dotenv
import os


load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

# --------------------------
# BACKEND CALLS
# --------------------------

def handle_input_ba(message: Dict[str, Any], 
                 history: Optional[List] = None, 
                 metadata_state: Optional[List] = None,
            ) -> Tuple[str, List]:
    
    payload = {
        "message": message,
        "history": history,
        "metadata_state": metadata_state,
    }

    response = requests.post(f"{FASTAPI_URL}/ba_handle_input", json=payload)
    data = response.json()
    print(data)
    print(type(data))
    return data


def remove_instance_ba(metadata_state: gradio.State):
    """
    Called when Gradio session closes. 
    This calls FastAPI /ba_remove_instance to remove the agent session.
    """
    requests.post(f"{FASTAPI_URL}/ba_remove_instance", json={
        "metadata_state": metadata_state
    })


def handle_input_account(message: Dict[str, Any], 
                 history: Optional[List] = None, 
                 metadata_state: Optional[List] = None,
            ) -> Tuple[str, List]:
    
    payload = {
        "message": message,
        "history": history,
        "metadata_state": metadata_state,
    }

    response = requests.post(f"{FASTAPI_URL}/account_handle_input", json=payload)
    data = response.json()
    print(data)
    print(type(data))
    return data


def remove_instance_account(metadata_state: gradio.State):
    """
    Called when Gradio session closes. 
    This calls FastAPI /ba_remove_instance to remove the agent session.
    """
    requests.post(f"{FASTAPI_URL}/account_remove_instance", json={
        "metadata_state": metadata_state
    })


with gradio.Blocks(title="Finance AI") as demo:
    go_to_ba_agent_button = gradio.Button("BA Agent")
    go_to_account_agent_button = gradio.Button("Account Agent")

    go_to_ba_agent_button.click(None, None, None, js="() => {window.location.href = '/ba_agent';}")
    go_to_account_agent_button.click(None, None, None, js="() => {window.location.href = '/account_agent';}")

with demo.route("Account Agent", "/account_agent"):
    metadata_state = gradio.State([], delete_callback=lambda x: remove_instance_account(x))
    with gradio.Column(elem_id="tips-column"):
        gradio.Markdown("## Tips and Tricks To Help You Interact With The Agent", elem_id="tips-header")
        gradio.Markdown("""
            - **Ask specific questions**: The more specific you are, the better the answer! \t For example: **Use company names, Use Dates** *'What is the cashflow for Whirlpool for the most recent available quarter?'*
            - **Financial Analysis**: You can ask for balance sheets, P&L statements, and more!
            - **Sales Data**: Sales data is pulled the moment you start chatting, if you come back to a window after a few days, just refresh the tab to get up-to-date data.
        """, elem_id="tips-body")
    with gradio.Column(elem_id='chat-column'):
        gradio.ChatInterface(
            fn=handle_input_account,
            multimodal=True,
            title="Accounting Agent",
            additional_inputs=[metadata_state],
            additional_outputs=[metadata_state],
            examples=[
                ["What is the total dollar value of all non-cancelled orders opened by Amazon this month?"], 
                ["I'm risk-averse, is Whirlpool or Frontdoor Inc. more likely to lose money next year?"], 
                ["Give me the cashflow statement for Whirlpool for the year 2024"]
            ],
        )

with demo.route("BA Agent", "/ba_agent") as ba_page:
    metadata_state = gradio.State([], delete_callback=lambda x: remove_instance_ba(x))
    with gradio.Column(elem_id="tips-column"):
        gradio.Markdown("## Tips and Tricks To Help You Interact With The Agent", elem_id="tips-header")
        gradio.Markdown("""
            - **Ask specific questions**: The more specific you are, the better the answer! \t For example: **Use company names, Use Dates** *'What is the cashflow for Whirlpool for the most recent available quarter?'*
            - **Financial Analysis**: You can ask for balance sheets, P&L statements, and more!
            - **Sales Data**: Sales data is pulled the moment you start chatting, if you come back to a window after a few days, just refresh the tab to get up-to-date data.
        """, elem_id="tips-body")
    with gradio.Column(min_width=300, elem_id='chat-column'):
        gradio.ChatInterface(
            fn=handle_input_ba,
            multimodal=True,
            title="BA Agent",
            additional_inputs=[metadata_state],
            additional_outputs=[metadata_state],
            examples=[
                ["What is the most profitable stove we sell to Sears?"], 
                ["I'm risk-averse, is Whirlpool or Frontdoor Inc. more likely to lose money next year?"], 
                ["Give me the cashflow statement for Whirlpool for the year 2024"]
            ],
        )


demo.launch(server_name="0.0.0.0", server_port=7860, css_paths="chat_style.css",)