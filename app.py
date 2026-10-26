import json
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_SCHEMAS, call_tool

load_dotenv()

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="ALIYU SAIDU | AI AGENT", page_icon="🏛️"
)
st.title("🏛️ ALIYU SAIDU — AI AGENT")
st.caption(
    "Public Sector Executive | Strategic Administrator | Health Systems Leader"
)

SYSTEM_PROMPT = """You are an official Executive AI Assistant representing Aliyu Saidu.
Your task is to answer professional inquiries about Aliyu Saidu's career, qualifications, administrative experience, and public leadership.

Rules:
1. ALWAYS use your available tools to verify facts about Aliyu Saidu before answering.
2. Maintain an authoritative, respectful, and highly professional executive tone.
3. If asked about information not present in the tools, state clearly that you only provide verified biographical and professional context regarding Aliyu Saidu.
4. Show clear, concise summaries when tools return output."""


# ----------------------------------------------------------------------
# API key retrieval (env or Streamlit secrets)
# ----------------------------------------------------------------------
def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None


api_key = get_api_key()
if not api_key:
    st.error(
        "No API key found. Add OPENAI_API_KEY to your .env file (local) "
        "or to your Streamlit Cloud secrets (deployed)."
    )
    st.stop()

client = OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"


# ----------------------------------------------------------------------
# Conversation memory
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Replay conversation
for msg in st.session_state.messages:
    role = msg["role"] if isinstance(msg, dict) else msg.role
    if role in ("user", "assistant"):
        content = msg["content"] if isinstance(msg, dict) else msg.content
        if content:
            with st.chat_message(role):
                st.markdown(content)


# ----------------------------------------------------------------------
# Chat input + Agent Tool Loop
# ----------------------------------------------------------------------
if prompt := st.chat_input("Ask about Aliyu Saidu's career, education, or leadership..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        # --- The Agent Loop ---
        with st.status("Consulting biographical records...", expanded=True) as status:
            while True:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    tools=TOOL_SCHEMAS,
                )
                message = response.choices[0].message

                if not message.tool_calls:
                    break

                st.session_state.messages.append(message)

                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    st.write(f"🔧 Tool invoked: **{name}**")

                    try:
                        result = call_tool(name, args)
                    except Exception as e:
                        result = f"Tool error: {e}"

                    st.write(f"↳ {result}")
                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })

            status.update(label="Information retrieved!", state="complete", expanded=False)

        # --- Stream final response ---
        def stream_answer():
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                if piece:
                    yield piece

        answer = st.write_stream(stream_answer())
        st.session_state.messages.append({"role": "assistant", "content": answer})


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("About the Agent")
    st.write(
        "This AI agent serves as an interactive professional assistant for **Aliyu Saidu**, "
        "leveraging custom tools to retrieve factual career data from his biography."
    )
    st.markdown("---")
    st.write("**Key Capabilities:**")
    st.write("- Query current KMDC leadership profile")
    st.write("- Explore past leadership at KADCHMA, SURE-P, NIMC, NHS")
    st.write("- Verify UK & Nigerian educational credentials")
    st.write("- Retrieve political & public service background")
    st.markdown("---")
    if st.button("Reset Conversation"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()