Let's make a swarm of LLM agents to create and manage a pipeline to give both patients and medical providers a system assisting in returning medical answers to patients. There are a few requirements as follows: The patient agent will initiate the question. The medical provider will need to agree to the answer generated from an agent. The medical answers will need to have some patient context access such as a medical chart. Currently we will have a source of synthetic patient data stored in a directory for access. Most questions will be about some specific result in the chart and so the LLm assisting with the patients will need to query the database or patent chart prior to generating the answer. Please understand that most patients will ask a question that is not clear from the start. We will likely need to identify what assumptions have been made and minimize and assumptions that might misdirect the conversation and answers. We therefor might need a conversation bot if the question is unclear. I want to insure we get the best possible answers delivered to the patient and providers. Once we have a clear question from the patent then we will need to query the correct patient data and any relevant past data. Once the data has been retrieved then we can generate a response from the question and necessary data. At this point the provider will evaluate the response and make corrections if needed. The medical response or answer will need to be returned to the patient in a clear and processed manor that the general public can understand. I want help creating a swarm of agents for each of these tasks. I will need a LLM agent described for each above task with an evaluating agent at each step. For testing purposes let's also make a patient LLM and a medical provider LLM and later we will force a real provider like myself to sign the message prior to sending back to the patient. We are not trying to classify the medical queries. we are attempting to assist the medical provider in giving relevant answers to a patient.  One GPT will clarify with the patient if the question is not clear. Then we will pass off the clarified question to a new GPT that will access the patient's chart and process the question and relevant chart data and then generate a response that can be reviewed by the provider (outside this scope but the provider will sign the response) This signed response will then be returned to the patient for review. It takes a lot of time for providers to give answers to the patient mostly due to miscommunication and the requirement to type the responses. We are generating a system of GPT's to assist both provider and patient in communicating successfully while providing a medically relevant response that is accurate above all. We will need to generate prompts for these tasks and a supervising GPT to run in parallel to make sure the data used from the chart is accurate and relevant to the question. The GPT will need respond to the patient follow up questions. 

### Patient Question Agent:
Task: Act like a patient and generate a question basised on current results in the chart.
Tools: NLP toolkit. FHIR protocol. It will randomly pick a chart and generate a question based on the one of the recoent results.
Input: List of patient charts. 
Output: Generate a question and then forwarded queries to the Query Clarification Agent.

### Supervising Agent
Task: Ensure data accuracy and relevance throughout the process.
Tools: Monitoring and validation tools.
Input: Data and actions from all other agents.
Output: Verifications and error corrections.
Example Prompt: You are the Supervising Agent. Your task is to monitor the entire process, ensuring that all data used is accurate and relevant to the patient's query. Address any discrepancies or issues that arise.

### Data Retrieval Agent

Task: Query the synthetic patient data directory to retrieve relevant patient information.
Tools: Database query toolkit, access to synthetic patient data.
Input: Clarified queries from the Query Clarification Agent.
Output: Retrieved data to the Response Generation Agent.
Example Prompt:
You are the Data Retrieval Agent. Your task is to retrieve relevant patient data from the synthetic data directory based on the clarified query. Ensure the data is accurate and relevant to the query.