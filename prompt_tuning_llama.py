# coding: utf-8
# Copyright (c) 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# prompt_tuning.py
# Supports Python 3
##########################################################################
# Description:
# This script extracts structured JSON data from unstructured text descriptions
# using Oracle Cloud Infrastructure (OCI) Generative AI Service.
# 
# It demonstrates how to:
# 1. Define a JSON schema for structured data extraction
# 2. Create a prompt with specific instructions for the LLM
# 3. Process and validate the LLM's response
# 4. Extract and save the resulting JSON data
##########################################################################
# Author:   Francesco Salerno
# Date:     2023-08-01
# Language: Python
# SDK:      OCI Python SDK
# API:      Generative AI Service
##########################################################################

import oci
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup basic variables
# Auth Config
compartment_id = os.getenv('COMPARTMENT_ID')
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Service endpoint
endpoint = "https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com"

# Sample tree evaluation description
tree_evaluation = """
L'albero ritratto nella fotografia sembra appartenere al genere Aesculus, con buona probabilità 
si tratta di un Aesculus hippocastanum, comunemente noto come ippocastano. Sebbene l'identificazione 
definitiva richiederebbe una visione ravvicinata delle foglie o dei frutti, la morfologia generale 
suggerisce questa specie.
Le foglie, di colore verde intenso e dall'aspetto sano, appaiono composte e palmate, con una
disposizione regolare e abbondante lungo tutta la chioma. La chioma stessa presenta una forma
tondeggiante, simmetrica e ben sviluppata, con una densità elevata che garantisce una copertura 
uniforme. Le dimensioni della chioma sono compatibili con quelle di un albero maturo in ambiente 
urbano, con un diametro stimabile tra i quattro e i sei metri.
Il tronco, diritto e di colore grigio chiaro, risulta proporzionato all'insieme dell'albero, 
privo di segni evidenti di danni o patologie. Le ramificazioni principali partono a una certa altezza, 
contribuendo a mantenere uno spazio libero alla base, caratteristica spesso favorita negli esemplari 
collocati in aree pubbliche come parchi o giardini.
Le radici non sono visibili nella fotografia e non è quindi possibile una valutazione diretta.
Tuttavia, l'assenza di sollevamenti del terreno o di danni al manto erboso circostante suggerisce 
un apparato radicale ben sviluppato ma non eccessivamente invasivo in superficie.
Nel complesso, l'albero appare in ottimo stato fitosanitario. Non sono presenti segni di disseccamento, 
ingiallimenti anomali o diradamenti nella chioma. L'aspetto generale è vigoroso e ben mantenuto, 
pienamente integrato nell'ambiente urbano in cui si trova.
"""

# Define the expected JSON schema
schema_json = {
  "identificazione": {
    "genere": "string",
    "specie_probabile": "string",
    "nome_comune": "string",
    "certezza_identificazione": "string",        
    "note_identificazione": "string"
  },
  "foglie": {
    "colore": "string",
    "tipo": "string",                             
    "disposizione": "string",                      
    "aspetto": "string"                            
  },
  "chioma": {
    "forma": "string",                             
    "densita": "string",                          
    "copertura": "string",
    "diametro_stimato_m": {
      "minimo": "float",
      "massimo": "float"
    },
    "sviluppo": "string"                          
  },
  "tronco": {
    "colore": "string",
    "posizione": "string",                         
    "proporzioni": "string",
    "condizione": "string",                        
    "ramificazione": {
      "altezza_inizio": "string",                 
      "caratteristica": "string"                   
    }
  },
  "radici": {
    "visibilità": "boolean",
    "presenza_danni_superficie": "boolean",
    "note": "string",
    "valutazione_indiretta": "string"
  },
  "contesto": {
    "ambiente": "string",                          
    "tipologia": "string",                         
    "integrazione_ambientale": "string"
  },
  "salute": {
    "stato_generale": "string",                    
    "segni_negativi": {
      "disseccamenti": "boolean",
      "ingiallimenti": "boolean",
      "diradamenti": "boolean"
    },
    "vigore": "string",                            
    "manutenzione": "string",
    "integrazione_estetica": "string"
  }
}


# Define permitted values for certain fields
permitted_values = {
    "certezza_identificazione": ["certa", "probabile", "ipotetica", "non identificata"],
    "tipo foglie": ["semplici", "composte", "composte palmate", "composte pennate"],
    "disposizione foglie": ["regolare", "irregolare", "densa", "sparsa"],
    "forma chioma": ["tondeggiante", "piramidale", "conica", "espansa", "globosa", "irregolare"],
    "densita chioma": ["alta", "media", "bassa"],
    "copertura chioma": ["uniforme", "non uniforme", "asimmetrica"],
    "posizione tronco": ["eretto", "inclinato", "contorto"],
    "altezza_inizio_ramificazione": ["bassa", "media", "alta"],
    "visibilita radici": [True, False],
    "presenza_danni_superficie": [True, False],
    "ambiente": ["urbano", "rurale", "forestale", "parco", "giardino"],
    "tipologia": ["parco pubblico", "giardino privato", "bordo strada", "piazza", "area scolastica"],
    "stato_generale": ["ottimo", "buono", "discreto", "scarso", "critico"],
    "disseccamenti": [True, False],
    "ingiallimenti": [True, False],
    "diradamenti": [True, False],
    "vigore": ["alto", "medio", "basso"],
    "manutenzione": ["ottima", "buona", "scarsa", "assente"]
}

def extract_and_save_json(text, output_path):
    """Extract JSON from text and save it to a file"""
    try:
        # First attempt: try to parse as-is
        json_response = json.loads(text)
        
    except json.JSONDecodeError:
        # Second attempt: try to extract JSON using regex
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if not match:
            print("Could not extract JSON from response")
            return None
            
        try:
            json_response = json.loads(match.group(1))
        except json.JSONDecodeError:
            print("Could not parse extracted JSON")
            return None
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(json_response, f, indent=2)
    print(f"JSON saved to {output_path}")
    
    return json_response

# Construct the prompt with the schema and permitted values
prompt_template = f"""
Sei un esperto nella valutazione degli alberi. Analizza la seguente descrizione di valutazione dell'albero ed estrai le informazioni rilevanti in un formato JSON strutturato.

DESCRIZIONE:
{tree_evaluation}

SCHEMA DI OUTPUT:
{json.dumps(schema_json, indent=2)}

VALORI CONSENTITI:
{json.dumps(permitted_values, indent=2)}

ISTRUZIONI:

1. Estrai tutte le informazioni rilevanti dalla descrizione.
2. Formattta l'output secondo lo schema JSON fornito.
3. Per i campi con valori consentiti, utilizza solo i valori presenti nell'elenco.
4. Se l'informazione non è disponibile nella descrizione, usa null come valore.
5. Converti le misure in numeri senza unità (es: "15 metri" diventa 15).
6. Assicurati che l'output sia un JSON valido.
7. Restituisci SOLO il risultato in JSON, senza alcun testo o spiegazione aggiuntiva.
"""

print(prompt_template)

# Initialize the client
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config=config, 
    service_endpoint=endpoint, 
    retry_strategy=oci.retry.NoneRetryStrategy(), 
    timeout=(10,240)
)

# Prepare the chat request
chat_detail = oci.generative_ai_inference.models.ChatDetails()
content = oci.generative_ai_inference.models.TextContent()
content.text = prompt_template
message = oci.generative_ai_inference.models.Message()
message.role = "USER"
message.content = [content]

chat_request = oci.generative_ai_inference.models.GenericChatRequest()
chat_request.api_format = oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC
chat_request.messages = [message]
chat_request.max_tokens = 4000
chat_request.temperature = 0.2  # Lower temperature for more deterministic JSON output
chat_request.frequency_penalty = 0
chat_request.presence_penalty = 0
chat_request.top_p = 0.95

chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
    model_id="ocid1.generativeaimodel.oc1.eu-frankfurt-1.amaaaaaask7dceya4tdabclcsqbc3yj2mozvvqoq5ccmliv3354hfu3mx6bq" # model: meta.llama-3.3-70b-instruct
)

chat_detail.chat_request = chat_request
chat_detail.compartment_id = compartment_id

# Send the request
chat_response = generative_ai_inference_client.chat(chat_detail)

# Process the response
response_text = chat_response.data.chat_response.choices[0].message.content[0].text
#print(response_text)

# Extract and save JSON
json_response = extract_and_save_json(
    response_text, 
    './samples/extracted_tree_data_llama.json'
)

if json_response:
    print("\n**************************Formatted JSON**************************")
    print(json.dumps(json_response, indent=2))
