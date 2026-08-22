import streamlit as st
from huggingface_hub import InferenceClient

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI Code Assistant")
st.write(
    "A Generative AI coding assistant for college laboratory students."
)

st.divider()

# -----------------------------
# Hugging Face API
# -----------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(
    api_key=HF_TOKEN
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙️ Options")

language = st.sidebar.selectbox(
    "Programming Language",
    [
        "Python",
        "C",
        "C++",
        "Java",
        "JavaScript"
    ]
)

task = st.sidebar.selectbox(
    "Choose Task",
    [
        "Generate Code",
        "Explain Code",
        "Debug Code",
        "Convert Code"
    ]
)

# -----------------------------
# Main Input
# -----------------------------
st.subheader("💻 Enter Your Request")

user_input = st.text_area(
    "Describe your programming problem:",
    height=180,
    placeholder="Example: Write a Python program to check whether a number is prime."
)

# -----------------------------
# Generate Button
# -----------------------------
if st.button("🚀 Generate", use_container_width=True):

    if not user_input.strip():
        st.warning("Please enter a programming question.")
    else:

        # Create prompt based on selected task
        if task == "Generate Code":

            prompt = f"""
You are an AI coding assistant for college students.

Generate a correct {language} program for the following problem:

{user_input}

Provide:
1. Complete code
2. Short explanation
3. Example input and output

Keep the explanation simple and suitable for a college laboratory.
"""

        elif task == "Explain Code":

            prompt = f"""
You are an AI programming tutor.

Explain the following {language} code in simple language:

{user_input}

Explain:
1. Purpose of the program
2. Important lines
3. How the program works
4. Example output
"""

        elif task == "Debug Code":

            prompt = f"""
You are an AI debugging assistant.

Find and fix errors in the following {language} code:

{user_input}

Provide:
1. Errors found
2. Corrected code
3. Explanation of the corrections
"""

        else:

            prompt = f"""
You are an AI programming assistant.

Convert the following code into {language}:

{user_input}

Provide:
1. Converted code
2. Short explanation
"""

        # -----------------------------
        # Call Hugging Face Model
        # -----------------------------
        with st.spinner("🤖 AI is working..."):

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI coding assistant. "
                        "Give accurate and beginner-friendly programming answers."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            try:

                response = client.chat_completion(
                    messages=messages,
                    model="Qwen/Qwen2.5-Coder-32B-Instruct",
                    max_tokens=1500,
                    temperature=0.2
                )

                answer = response.choices[0].message.content

                st.subheader("💡 AI Response")
                st.markdown(answer)

            except Exception as e:

                st.error(
                    "Something went wrong while connecting to "
                    "the Hugging Face API."
                )

                st.write(e)

st.divider()

st.caption("AI Code Assistant | College Laboratory Project")
