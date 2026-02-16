import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import time
import json
from dotenv import load_dotenv, find_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI
from utils.utils import convert_to_numeric, handling_problematic_data, read_json_to_df, format_time_columns,calculating_other_agencies, determine_next_day

PATH = "../../data/all_incidents.json"

def load_api():
    # read local .env file
    _ = load_dotenv(find_dotenv()) 
    api_key = os.environ['MISTRAL_API_KEY']
    return api_key

def initialise_model():
    model = ChatMistralAI(
        model = "mistral-large-latest", 
        temperature=0,
        max_retries=2
        )
    return model

def create_system_msg():
    msg = """
    You are to read reports of mountain rescue and identify the number of human victims and animal victims in each rescue. 
    You only need to give me the number of human victims and animal victims in a tuple in order, so I could put it into a database, without further processing. 
    If no mention of animals, please put 0 for the number representing the animal in the tuple. 
    If you are unsure of any of the number, please put -1 for the number representing the human victims or animal victims in the tuple.
    for example, if 1 victim is found, but no mention of animal, then the tuple will be (1,0), if you are unsure of the number of victims, and no animal found, then the tuple will be (-1,0)
    """
    return msg

def create_human_msg(main_text):
    # reduce the amount of text that llm needs to read by only taking the first two sentences of the incident reports
    print(main_text)
    if main_text !='':
        main_text = main_text.replace('No.', 'number')
        sent_list = (main_text).split('.')
        if len(sent_list)>1:
            first_two_sent = sent_list[0] + '. ' + sent_list[1]
            return first_two_sent
        else:
            return main_text
    elif main_text == '':
        return 'no mountain rescue report found.'

def create_response(model,system_msg, human_msg):
    try:
        response = model.invoke([SystemMessage(system_msg), HumanMessage(human_msg)])
        return response.content
    except Exception as e:
        print('An error occured ' + str(e))
        return (-1,-1)

def create_victim_value(df, model, system_msg):

    for idx, incident_text in enumerate(df.main_text):
        if idx > 7:
            human_msg = create_human_msg(incident_text)
            response = create_response(model,system_msg, human_msg)
            print(idx)
            print(df.iloc[idx]['Incident'])
            row_dict = {}
            row_dict['Incident'] = df.iloc[idx]['Incident']
            row_dict['victims'] = response

            with open('victims_2024.json','a') as file:
                json.dump(row_dict,file)
                file.write(', ')
            time.sleep(60)
            

def main():
    api_key = load_api()
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    data = convert_to_numeric(data)
    data = handling_problematic_data(data)
    
    data = data[(data['year']>2023) & (data['year']<2025)]

    system_msg = create_system_msg()
    model = initialise_model()
    data = create_victim_value(data, model, system_msg)

    print('finish')

main()

