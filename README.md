# LocalQ
A research tools that connects local LLMs to your database to perform safe and quick qualitative analysis. 

This tool is super symple and it will allow you to perform to following type of analysis:
 - Sentiment Analysis
 - Emotion Analysis
 - Thematic Analysis
 - Manual Thematic Analysis (you pick the themes)
 - Custom Propmt

You upload a csv file with two columns: Name/ID	& Text
Then you pick the type of analysis and it will return a new csv file with an additional column with the results.

For each raw, it will run a new instance in the local LLM through ollama, you can select the model that works best for your data and/or that works with your computer. Since it runs a new instance for each line, it works with small models and does not need lots of RAM / a powerful GPU. I tested it on a Mac Mini with only 8Gb of ram and it worked with both Gemma 2:2b and with Llama 3.2.

How to use this for newbies - Instructions for a Mac.

You will need to install ollama and python

  In the terminal type:
    ollama serve

  Then type (only the first time) to install the dependencies
    pip install streamlit requests pandas

  Then type

    cd Name_of_Directory_with_repository
  
  Then you will create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate

  Then type the following to start the app
    streamlit run app.py
  
You need to download at least one model in ollama by typing the following (change the name of the model to the one you prefer)
    ollama pull llama3.2
and then within the app you need to type the exact name of the model in the sidebar. To check the model you have installed, type in the terminal:
    ollama list


