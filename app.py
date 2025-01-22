# app.py

import streamlit as st
import pandas as pd
import re
import json
from ollama_utils import run_ollama

def main():
    st.title("My Ollama LLM App")

    # Sidebar: Model choice
    st.sidebar.subheader("Ollama Settings")

    # Model name text input
    model_name = st.sidebar.text_input(
        "Pick a Model (e.g., llama2, llama2:13b, etc.)",
        "llama2"
    )

    # Explanation & slider for Temperature
    st.sidebar.markdown(
        "**Temperature** controls how random or 'creative' the model is. "
        "Lower values (e.g., 0.0) make it more deterministic, while higher values "
        "(closer to 1.0) increase randomness and variety in the responses."
    )
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    # Explanation & input for Max Tokens
    st.sidebar.markdown(
        "**Max Tokens** is the maximum number of tokens (roughly pieces of words) "
        "the model can generate in a single response. Increasing this number allows for "
        "longer answers, but can also be slower or use more resources."
    )
    max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=2048, value=512)

    st.write("## 1. Upload CSV")
    uploaded_file = st.file_uploader("Upload a CSV with columns 'Name/ID' and 'Text'", type=["csv"])
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview:")
        st.dataframe(df.head())

        st.write("## 2. Choose Operation")
        analysis_option = st.selectbox(
            "What do you want to do?",
            [
                "Sentiment Analysis",
                "Emotion Analysis",
                "Thematic Analysis",
                "Manual Thematic Analysis",
                "Custom Prompt"
            ]
        )

        # ----------------------
        # SENTIMENT ANALYSIS
        # ----------------------
        if analysis_option == "Sentiment Analysis":
            if st.button("Run Sentiment Analysis"):
                results = []
                for i, row in df.iterrows():
                    text = row["Text"]
                    prompt = f"""
                    You are an academic researcher with expertise in qualitative analysis. Analyze the sentiment of the following text.
                    Return a valid JSON object with this key ONLY:
                    {{
                        "Overall Sentiment": "Positive"  # or "Negative", or "Neutral"
                    }}
                    Do not include any other text outside of this JSON object.

                    Text:
                    "{text}"
                    """

                    response = run_ollama(
                        prompt=prompt,
                        model=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                    # Ensure response is string
                    if not isinstance(response, str):
                        response = str(response) if response else ""

                    # Remove any code fences
                    cleaned = re.sub(r"```(\w+)?", "", response)

                    # Try parse JSON
                    try:
                        parsed = json.loads(cleaned.strip())
                    except json.JSONDecodeError:
                        parsed = {}

                    overall_sentiment = parsed.get("Overall Sentiment", "Unknown")

                    results.append({
                        "Name/ID": row["Name/ID"],
                        "Text": text,
                        "Overall Sentiment": overall_sentiment
                    })

                results_df = pd.DataFrame(results)
                st.write("### Sentiment Analysis Results")
                st.dataframe(results_df)

        # ----------------------
        # THEMATIC ANALYSIS
        # ----------------------
        elif analysis_option == "Thematic Analysis":
            if st.button("Run Thematic Analysis"):
                results = []
                for i, row in df.iterrows():
                    text = row["Text"]
                    prompt = f"""
                    You are a helpful assistant. Please extract two themes from the text below.

                    Return a valid JSON object with these keys ONLY:
                    {{
                        "Main Theme": "",
                        "Alternative Theme": ""
                    }}

                    Do not include any extra text or formatting.

                    Text:
                    {text}
                    """

                    response = run_ollama(
                        prompt=prompt,
                        model=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                    # Try parse JSON
                    try:
                        parsed = json.loads(response)
                        main_theme = parsed.get("Main Theme", None)
                        alt_theme = parsed.get("Alternative Theme", None)
                    except:
                        main_theme = None
                        alt_theme = None

                    results.append({
                        "Name/ID": row["Name/ID"],
                        "Text": text,
                        "Main Theme": main_theme,
                        "Alternative Theme": alt_theme
                    })

                results_df = pd.DataFrame(results)
                st.write("### Thematic Analysis Results")
                st.dataframe(results_df)

        # ----------------------
        # EMOTION ANALYSIS
        # ----------------------
        elif analysis_option == "Emotion Analysis":
            st.write(
                "This will identify the single most appropriate emotion for each row's text "
                "(e.g., anger, love, passion, hate, etc.)."
            )

            if st.button("Run Emotion Analysis"):
                results = []
                for i, row in df.iterrows():
                    text = row["Text"]
                    prompt = f"""
                    You are an academic researcher with expertise in qualitative analysis. 
                    Identify the single best-fitting emotion from the text below 
                    (e.g., anger, joy, love, sadness, hate, fear, passion, etc.).

                    Return a valid JSON object with this key ONLY:
                    {{
                        "Emotion": "example_emotion"
                    }}
                    Do not include any other text outside of this JSON object.

                    Text:
                    "{text}"
                    """

                    response = run_ollama(
                        prompt=prompt,
                        model=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                    # Ensure response is string
                    if not isinstance(response, str):
                        response = str(response) if response else ""

                    # Remove any code fences
                    cleaned = re.sub(r"```(\w+)?", "", response)

                    # Try parse JSON
                    try:
                        parsed = json.loads(cleaned.strip())
                    except json.JSONDecodeError:
                        parsed = {}

                    emotion = parsed.get("Emotion", "Unknown")

                    results.append({
                        "Name/ID": row["Name/ID"],
                        "Text": text,
                        "Emotion": emotion
                    })

                results_df = pd.DataFrame(results)
                st.write("### Emotion Analysis Results")
                st.dataframe(results_df)

        # ----------------------
        # MANUAL THEMATIC ANALYSIS
        # ----------------------
        elif analysis_option == "Manual Thematic Analysis":
            st.write(
                "Provide up to 10 themes (comma-separated). For each row, "
                "the app will pick the single best-fitting theme."
            )
            
            # Let user input themes (comma-separated)
            user_themes = st.text_input(
                "Enter up to 10 themes, separated by commas:",
                "Theme1, Theme2, Theme3"
            )

            # Convert user input to a list of themes (strip spaces)
            themes_list = [t.strip() for t in user_themes.split(",") if t.strip()]

            # Validate we don't exceed 10
            if len(themes_list) > 10:
                st.error("Please enter no more than 10 themes.")
            else:
                if st.button("Run Manual Thematic Analysis"):
                    results = []
                    for i, row in df.iterrows():
                        text = row["Text"]
                        # Create a comma list of themes for the prompt
                        themes_text = ", ".join(themes_list)

                        prompt = f"""
                        You are an academic researcher with expertise in thematic analysis.
                        We have a set of possible themes:
                        {themes_text}

                        Pick exactly ONE of the above themes that best fits the text below.
                        Return a valid JSON object with this key ONLY:
                        {{
                            "Chosen Theme": "theme_from_the_list"
                        }}
                        Do not add any extra text outside of this JSON object.

                        Text:
                        "{text}"
                        """

                        response = run_ollama(
                            prompt=prompt,
                            model=model_name,
                            temperature=temperature,
                            max_tokens=max_tokens,
                        )

                        # Ensure response is string
                        if not isinstance(response, str):
                            response = str(response) if response else ""

                        # Remove any code fences
                        cleaned = re.sub(r"```(\w+)?", "", response)

                        # Try parse JSON
                        try:
                            parsed = json.loads(cleaned.strip())
                        except json.JSONDecodeError:
                            parsed = {}

                        chosen_theme = parsed.get("Chosen Theme", "None")

                        results.append({
                            "Name/ID": row["Name/ID"],
                            "Text": text,
                            "Chosen Theme": chosen_theme
                        })

                    results_df = pd.DataFrame(results)
                    st.write("### Manual Thematic Analysis Results")
                    st.dataframe(results_df)

        # ----------------------
        # CUSTOM PROMPT
        # ----------------------
        else:  # "Custom Prompt"
            custom_prompt = st.text_area(
                "Enter your custom prompt (use [Text] as a placeholder for each row's text):",
                "Summarize the following text: [Text]"
            )
            if st.button("Run Custom Prompt"):
                results = []
                for i, row in df.iterrows():
                    text = row["Text"]
                    final_prompt = custom_prompt.replace("[Text]", text)

                    response = run_ollama(
                        prompt=final_prompt,
                        model=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )

                    results.append({
                        "Name/ID": row["Name/ID"],
                        "Text": text,
                        "Custom Prompt Output": response
                    })

                results_df = pd.DataFrame(results)
                st.write("### Custom Prompt Results")
                st.dataframe(results_df)


if __name__ == "__main__":
    main()
