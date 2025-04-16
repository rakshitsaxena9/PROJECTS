from geminiapi import LinkdIn_Summarizer
import pandas as pd
import numpy as np 
from random import randint
from time import sleep 
import dotenv 
import re
from rouge_score import rouge_scorer
def output_generation():
    linkdIn_summarizer = LinkdIn_Summarizer()
    total_tone=list()
    total_target_summary= list()
    total_original_summary=list()
    file_name ='final_data.csv'
    with open(file_name,'r',encoding='utf8') as file:
        data= pd.read_csv(file)
    url_list= list()
    for i in range(0,100):
        profile_string= ""
        profile_data = dict(data.iloc[i])
        for key,value in profile_data.items():
            if (isinstance(value, (float, np.float64)) and np.isnan(value)) or (value=='[]') or key=='LinkedIN_Url':
                continue
            pattern = r"[\[\]{}'\\]"  
            profile_string += key.capitalize()+": " + re.sub(pattern,'',value)+"\n\n" 

        x = randint(a=1,b=3)
        word = randint(a=100,b=200)
        tone="professional"
        if x==1:
            tone="casual"
        elif x==2:
            tone= "motivational"
        response = linkdIn_summarizer.response_generator(profile_string,tone, word)
        total_original_summary.append(profile_data['summary'])
        total_tone.append(tone)
        total_target_summary.append(response)
        url_list.append(data['LinkedIN_Url'].iloc[i])
        if (i+1)%5 ==0:
            print(i+1) 
        sleep(8)
        
    output={'original_summary': total_original_summary,'target_summary': total_target_summary, 'tone':total_tone,'LinkedIN_Url':url_list}
    output_data= pd.DataFrame(output, columns=['original_summary','tone','target_summary','LinkedIN_Url'])
    output_data.to_csv('outputs/output_summary.csv', mode='a')

def score_evaluation():
    data= pd.read_csv('outputs/output_summary.csv',encoding='utf8',index_col=[0])
    data=data.fillna("")
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    score=[]
    for ref, gen in zip(data['original_summary'], data['target_summary']):
        scores = scorer.score(ref, gen)
        score.append(scores)
        # print(f"Reference: {ref}")
        # print(f"Generated: {gen}")
        print(f"ROUGE-1: {scores['rouge1'].fmeasure}, ROUGE-2: {scores['rouge2'].fmeasure}, ROUGE-L: {scores['rougeL'].fmeasure}\n")
    return score    
output_generation()
# score= score_evaluation()
