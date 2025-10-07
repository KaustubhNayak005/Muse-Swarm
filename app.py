import os
import streamlit as st
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function

# --- Import the tool function ---
from tools import generate_character_profile

# --- Avatar Dictionary ---
AVATARS = {
    "User": "🧑‍💻",
    "Project_Manager": "📋",
    "Creative_Muse": "🎨",
    "Critic": "🧐",
    "Unknown Agent": "🤖"
}

# --- App UI Setup ---
st.title("🎨 Creative Muse Swarm")

with st.sidebar:
    st.header("Configuration")
    load_dotenv()
    groq_api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))

    if not groq_api_key:
        st.warning("Please enter your Groq API key to begin.")
        st.stop()

# Initialize or display chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = AVATARS.get(message["name"])
    with st.chat_message(message["name"], avatar=avatar):
        st.markdown(message["content"])

# --- Main App Logic ---
if prompt := st.chat_input("Enter your creative prompt for the agent swarm..."):
    st.session_state.messages.append({"name": "User", "content": prompt})
    with st.chat_message("User", avatar=AVATARS.get("User")):
        st.markdown(prompt)

    with st.spinner("The agent swarm is thinking..."):
        # --- 1. Define LLM Configurations ---
        llm_config_reasoning = {
            "model": "qwen/qwen3-32b",
            "api_key": groq_api_key,
            "base_url": "https://api.groq.com/openai/v1",
        }

        llm_config_creative = {
            "model": "llama-3.3-70b-versatile",
            "api_key": groq_api_key,
            "base_url": "https://api.groq.com/openai/v1",
        }

        # --- 2. Define Agents with updated instructions ---
        project_manager = UserProxyAgent(
            name="Project_Manager",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )

        creative_muse = AssistantAgent(
            name="Creative_Muse",
            system_message=(
                "You are a creative muse. Your goal is to generate and refine creative concepts based on feedback. "
                "Incorporate the Critic's suggestions to improve your ideas. "
                "Only after the Critic has formally approved your idea should you provide a final summary and then say the word 'TERMINATE'."
            ),
            llm_config=llm_config_creative,
        )

        critic = AssistantAgent(
            name="Critic",
            system_message=(
                "You are a constructive film critic. Your job is to review ideas and suggest improvements. "
                "Your feedback should be concise and limited to 3-4 key bullet points. " # <-- CHANGE IS HERE
                "After providing your feedback, you MUST ask the Creative_Muse to provide a revised version incorporating your feedback. "
                "Do not approve an idea easily; always find something to improve."
            ),
llm_config=llm_config_creative,
        )

        # 3. Register the tool
        register_function(
            generate_character_profile,
            caller=creative_muse,
            executor=project_manager,
            name="generate_character_profile",
            description="Generate a detailed profile for a fictional character.",
        )

        # 4. Create the Group Chat
        agents = [project_manager, creative_muse, critic]
        groupchat = GroupChat(agents=agents, messages=[], max_round=10) # <-- CHANGE IS HERE
        manager = GroupChatManager(
            groupchat=groupchat, 
            llm_config=llm_config_reasoning
        )

        # 5. Initiate the chat
        project_manager.initiate_chat(
            recipient=manager,
            message=prompt,
        )
        
        # Get and display history
        chat_history = groupchat.messages
        for msg in chat_history:
            if msg['role'] == 'user':
                continue
            if msg.get("content", "").strip():
                agent_name = msg.get("name", "Unknown Agent")
                content = msg.get("content", "")
                avatar = AVATARS.get(agent_name)
                st.session_state.messages.append({"name": agent_name, "content": content})
                with st.chat_message(agent_name, avatar=avatar):
                    st.markdown(content)