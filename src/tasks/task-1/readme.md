# Task 1 : Report

Task 1 of our project **AI Chatbot for BRTS Navigation in Bhopal** , was Research & Data Collection. This report details the work done in the course of this task .

## What was discussed?
- Analyzed Bhopal's BRTS system and how exactly AI could play a positive role in it
- Gathered insights and information from chatbots/platforms deployed in similar public transit systems, for eg, Namma Metro(Bengaluru), Ahmedabad BRTS etc
- Discussed modes of deployment of chatbot

###  AI Model Exploration
 Several approaches were put forward for the chatbot's model Some of them were :
 - GPT Wrappers 
 - LSTMs
 - RAG model
 - Bi-LSTMs

## 2. Approaches Finalised
- Whatsapp was agreed as the mode of deployment due its already prevalent use and familiar interface
- GPT wrappers were rejected due to the unsustainibility of the credit system in the long run
- LSTMs are efficient and ideal for a system that handles structured queries like schedule lookups but lacks the conversational depth that is required in a chatbot
- RAG models give factual responses while maintaining a reasonable level of conversation, making them a good fit 

- BiLSTMs with an attention layer can ensure that the chatbot grasps the full meaning of user queries, capturing both past and future context, while giving personalized responses
## Which One is Better?

Consensus amongst the group leaned towards implementing a RAG mdoel for the following reasons :

- Combines real-time data retrieval with natural response generation.
- Delivers up-to-date and accurate transit info like schedules and routes.
- Maintains a conversational, user-friendly tone.
- Improves over time as more data is added.
- Efficiently handles large-scale information.
- Easier to implement than training a model from scratch, as it leverages existing data and retrieval mechanisms, saving time and resources.


However, the LSTM and GPT approaches are still being pursued parallelly alongside the RAG Model.

  
## References
- [BRTS_CaseStudy]((https://omdenavitb-brts.slack.com/files/U07Q8PVK55L/F07QU4ALR2P/pmi_casestudies__301120171204_bhopal-bus-rapid-transit-system.pdf))

- [BRT_Data](https://omdenavitb-brts.slack.com/files/U07Q8PVK55L/F07QU5NH3J9/brtdata-india.xlsx)
- [Overview_of_ChatbotTechnology](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7256567/)
- [Namma_Metro_WhatsappChatbot](https://medium.com/@papabot/revolutionizing-metro-travel-in-bengaluru-the-naama-metro-whatsapp-bot-ca208a57ac0f)
- [AIChatBot_inTransportationSystem](https://omdenavitb-brts.slack.com/files/U07Q5GCTSNS/F07RYAQCS8Y/ijcrt2110347.pdf?origin_team=T07HBQ1CX8B&origin_channel=C07HBQ1D96X)


## Active Contributors
- Tanisha Banik
- Shubha Ruidas
- Aryan Pahari
- Aditya Paul
