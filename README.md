LOCALQ
A research tool that connects local LLMs to your database (CSV file) to perform safe and quick qualitative analysis of large data set. The qualitive of the analysis will largely depend by the actual local LLM you pick.

======== FEATURES
This tool is super simple and allows you to perform the following types of analysis:
- Sentiment Analysis (3 outputs: positive, negative or neutral)
- Emotion Analysis (actual emotions like love, anger, etc.)
- Thematic Analysis
- Manual Thematic Analysis (you pick the themes up to 10)
- Custom Prompt (you write your own prompt, very useful for a variety of things)

Adjust token size and temperature for better results

![Screenshot 2025-01-21 at 9 53 41 PM](https://github.com/user-attachments/assets/c14f9d44-0271-4cd6-b94a-c788132ef58b)



======== HOW IT WORKS
1. Input:
   Upload a CSV file with two columns:
   - Name/ID
   - Text

2. Pick Analysis:
   Select the type of analysis you want to perform.

3. Output:
   The tool will return a new CSV file with an additional column containing the results.

For each row, LocalQ runs a new instance in the local LLM through Ollama.  
- You can select the model that works best for your data and/or your computer.  
- Since it processes one row at a time, it works well with smaller models and does not require much RAM or a powerful GPU.  
- Tested successfully on a Mac Mini (8GB RAM) with models like `Gemma 2:2b` and `Llama 3.2`.

======== GETTING STARTED
(MAC INSTRUCTIONS)

1. Prerequisites:
   - Install Ollama (for local LLM serving).
   - Install Python (if not already installed).

2. Start Ollama:
   Open your terminal and type:
ollama serve

3. Install Dependencies:
(Run this only the first time to install required Python libraries.)
pip install streamlit requests pandas

4. Navigate to the Repository:
Replace `Name_of_Directory_with_repository` with the actual path:
cd Name_of_Directory_with_repository

5. Set Up a Virtual Environment:
Create and activate the environment:
python3 -m venv venv source venv/bin/activate

6. Run the App:
Start the app with:
streamlit run app.py

======== DOWNLOADING MODELS IN OLLAMA
To use this app you need to have downloaded at least one model, use the following command:  
(Change `<model_name>` to the name of the model you want.)
ollama pull <model_name>

Find models here: https://ollama.com/search
