# AIzaSyAqrAuWnbAU6BzqarmXN4mGyrkXjkPwolo
# Import the Python SDK
# import google.generativeai as genai
import json 
import streamlit as st 
import os 
from dotenv import load_dotenv 
import pandas as pd
import numpy as np
import re
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

class LinkdIn_Summarizer:
    def __init__(self, model=None ,api_key=None, generation_config=None, system_instruction=None):
        """Initialize with dynamic API key, model type, generation config, and system instruction."""
        load_dotenv()
        self.api_key = api_key or self._load_api_key() 
        self.model_name = model or self._default_model_name()
        self.generation_config = generation_config or self._default_generation_config()
        self.system_instruction = system_instruction or self._default_system_instruction()
        self.model = self.configure_model()
    
    def _default_model_name(self):
        return os.getenv("GOOGLE_MODEL")
    def _load_api_key(self):
        """Load API key from environment variables."""
        
        return os.getenv("GOOGLE_API_KEY")
    def _default_generation_config(self):
        """Provide a default configuration for the generative model."""
        return  {
                "max_output_tokens": 2048,
                "temperature": 1.6,
                "top_p": 0.6,
                }


    def _default_system_instruction(self):
        """Provide a default system instruction for generating LinkedIn summaries."""
        return (
            """You are a writing a summary for your linkedIn Profile using 80-150 words in the most authentic and unique way possible.
Summary must contains very short paragraphs or lines having proper spacing between them.  
Emphasizing following points: 
1. Describe what makes you tick:
-Have you ever become so engaged in what you\'re doing at work that you lose track of time? What work activity(ies) bring that on?
-What\'s something you do for fun that uses the same or similar skills you use at work?
2. Explain your present role: What\'s the impact of you doing your job well versus not as well? 
3. Highlight your successes
4. Reveal your character: 
-What\'s your most unique quality?
-Is there anything your friends, family, or coworkers tease you about that you\'re secretly proud of? 
5. Show life outside of work:
-Is there anything you do for pleasure that makes you better at your job? Or give you a different perspective on it?
6. Make your first sentence count: This means no “Hi, I\'m Jane Smith and I\'m glad to meet you” and no “Thanks for visiting!” Don\'t waste precious characters on filler — cut right to the good stuff to pull your audience in.
7. Pump the keywords: keywords that highlight your top skills
8. Cut the jargon: Too many profiles read like: “Strategic, results-oriented professional with a proven track record of delivering results and a demonstrated history working in the XYZ industry.”
9. Create white space: More structured, easy to read in one glace."""
)

    def configure_model(self, model_name=None, generation_config=None, system_instruction=None):
        """
        Configure and return a Generative Model for generating LinkedIn summaries.
        
        Arguments:
            model_type (str): The type of model to use (default is "gemini-1.5-flash").
            generation_config (dict): The generation configuration for the model.
            system_instruction (str): The system instruction to guide the model.
        """
        vertexai.init(project="1070993788986", location="asia-southeast1")
        model_name = model_name or self.model_name
        system_instruction = system_instruction or self.system_instruction
        generation_config = generation_config or self.generation_config
        
        return GenerativeModel(
            model_name,
            system_instruction=system_instruction,
            generation_config = generation_config
        )
        
    def content_loader(self,file_name='datalib/Dan Morales.json',index=None):
        """
        Loads the data from csv and json files.
        Args:
            file_name (str, optional): Name of the file to load.
        Returns:
            _type_: dictionary
        """
        profile_string=""
        extention= os.path.splitext(file_name)[1]
        if extention==".json":
            with open(file_name,'r') as file:
                x= json.load(file)
            x['experience'] = x['jobHistory'][1]
            x['education'] = x['education'][1]
            x['skills']= ",".join(x['skills'])
            del x['jobHistory']
            order_list= ['name','experience','skills']
            # Get the remaining keys
            remaining_keys = [key for key in x if key not in order_list]
            # Create a new dictionary with the first two keys reordered
            ordered_dict = {key: x[key] for key in order_list + remaining_keys}
            for key,value in ordered_dict.items():
                if (isinstance(value, (float, np.float64)) and np.isnan(value)) or (value==[]):
                    continue
                profile_string += key.capitalize()+": " + value+"\n\n"
        #            
        if extention==".csv":    
            try:
                with open(file_name,'r',encoding='utf8') as file:
                    x= pd.read_csv(file)
                if index is None:
                    raise ValueError("Index cannot be None.")
                x =dict(x.iloc[index])
            except ValueError as ve:
                print(f"ValueError: {ve}")
            except FileNotFoundError:
                print(f"Error: The file '{file_name}' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            #Formatting the Data in string format.    
                for key,value in x.items():
                    if (isinstance(value, (float, np.float64)) and np.isnan(value)) or (value=='[]') or key=='LinkedIN_Url':
                        continue
                    pattern = r"[\[\]{}'\\]"  
                    profile_string += key.capitalize()+": " +re.sub(pattern,'',value)+"\n\n" 
        return profile_string
    def summary_generation_prompt(self,profile, tone=None,words=None):
        return f"""In {tone} tone including keywords related to career growth, industry and skills. Summarise the linkedIn profile in human written format.
        
        Details: {profile}.
        """
        
    def response_generator(self,profile, tone, words=100):
        """
        Generate the summary of the provided data.
        Args:
            profile (str): Containing details of the person for summary.
            tone (str): Define the tone of the output.
            words (int, optional): Word limit for the output. Defaults to 150.

        Returns:
            str: Summary of the profile
        """
        words = words if words>=70 else 100
        tone =  tone if tone.lower()=='professional' or tone.lower()=='casual' or tone.lower()=='motivational' else 'professional'
        prompt= self.summary_generation_prompt(profile, tone,words)
        response = self.model.generate_content(prompt, generation_config=self.generation_config)
        return response.text

if __name__=="__main__" :   
    st.set_page_config(page_title= "Profile Generator")
    st.header("Gemini Application")
    words= st.number_input("Words: ", key="words")
    tone= st.text_input("Tone: ", key="tone")
    submit = st.button("Give your File name")
    linkdIn_summarizer= LinkdIn_Summarizer()

    if submit:
        profile= linkdIn_summarizer.content_loader()
        response = linkdIn_summarizer.response_generator(profile,tone, words)
        st.subheader("The Response is")
        st.write(response)
    

