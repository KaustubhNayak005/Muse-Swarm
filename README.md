# 🎨 Creative Muse Swarm: An Advanced Agentic AI System

Creative Muse Swarm is a sophisticated multi-agent AI application designed to simulate a collaborative creative team. It leverages a "swarm" of specialized AI agents, orchestrated by a manager, to brainstorm, develop, and critique ideas in real-time. This project goes beyond simple chatbots to demonstrate a robust, tool-augmented, and multi-LLM agentic workflow.

---

## 🚀 Live Demo

**Try the live application here: https://kaustubhnayak005-muse-swarm-app-kuwniy.streamlit.app/**
---

## ✨ Key Features

- **Autonomous Multi-Agent Collaboration:** Employs a `GroupChat` architecture where specialized agents—a `Creative_Muse`, a `Critic`, and a `Project_Manager`—interact dynamically to iteratively refine ideas.

- **Intelligent Orchestration:** A `GroupChatManager` agent, powered by a reasoning-focused LLM (`qwen/qwen3-32b`), analyzes the conversation and directs the workflow, deciding which agent is best suited to speak next.

- **Layered AI & Dynamic Tool Use:** The `Creative_Muse` is equipped with a custom, **dynamic tool** that makes its own, separate LLM call. This demonstrates an advanced, layered architecture where a "manager" agent delegates a specialized generative task to a "specialist" AI function.

- **Specialized Multi-Model Strategy:** Utilizes a two-model approach to optimize performance. A powerful creative model (`llama-3.3-70b-versatile`) is used for content generation, while a different, reasoning-focused model is used for orchestration and analysis.

- **Interactive Web UI:** Built with Streamlit for a responsive and user-friendly experience, featuring unique avatars for each agent to clearly visualize the conversation.

## 🏛️ System Architecture

The workflow is designed to mimic a real creative team:

1.  The user provides a high-level prompt to the `Project_Manager`.
2.  The `Project_Manager` initiates a group chat, handing the task to the `GroupChatManager`.
3.  The `Manager` (**Reasoning LLM**) analyzes the prompt and delegates the initial task to the `Creative_Muse`.
4.  The `Creative_Muse` (**Creative LLM**) generates an idea and may decide to call its `generate_character_profile` tool.
5.  If a tool is called, the `Project_Manager` executes the function, which contains its own **Specialist LLM** call to generate a unique character.
6.  The `Manager` (**Reasoning LLM**) receives the results and delegates the task of feedback to the `Critic`.
7.  The `Critic` (**Creative LLM**) provides a detailed critique.
8.  This loop of generation and critique continues until the agents produce a satisfactory result.

## 🛠️ Tech Stack

- **Python**
- **AutoGen:** For the core multi-agent framework.
- **Groq API:** For high-speed LLM inference.
- **Streamlit:** For the interactive web UI.
- **Models:** `llama-3.3-70b-versatile` (Creative) & `qwen/qwen3-32b` (Reasoning).

## ⚙️ How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/KaustubhNayak005/Muse-Swarm.git](https://github.com/KaustubhNayak005/Muse-Swarm.git)
    cd Muse-Swarm
    ```

2.  **Set Up the Environment**
    ```bash
    python -m venv autogen-env
    .\autogen-env\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys**
    - Create a `.env` file in the root directory.
    - Add your Groq API keys:
      ```
      GROQ_API_KEY="gsk_..."
      GROQ_API_KEY_SPECIALIST="gsk_..."
      ```

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
