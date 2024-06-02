import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from swarms import Agent
from swarms.models import Anthropic
from swarms.models.gpt4_vision_api import GPT4VisionAPI
from swarms.structs.rearrange import AgentRearrange

# Load the environment variables
load_dotenv()


def MEDICAL_QUERY_CLASSIFICATION_AGENT() -> str:
    return """
    You are the Medical Query Classification Agent for the Patient-Question-Assist project. 
    Your task is to insure the question answered by the patient has enough detail to provide a good answer. 
    In the event that a patient asks a quesion with abiguity then your goal is to ask the patient for further details.
    You will chat with the patient to understand the question only if clarification is needed. 
    If the quesion is clear and specific then there is no need to clarify further.
    Once any question is clear and specific and so is answerable by the PATIENT_QUESTION_ASSIST agent then the clarified question will be passsed to the PATIENT_QUESTION_ASSIST agent.
    You will act as both a gate keeper and as as a clarifing agent. First is to clarify the question and know when to pass the question to the next agent = PATIENT_QUESTION_ASSIST agent.

### Input:
You will receive a JSON object with the following structure:
{
  "patient_id": "string",        # Unique identifier for the patient
  "query_id": "string",          # Unique identifier for the query
  "patient_question": "string"    # The query text from the patient
}



### Steps to Follow:
1. **Read and Understand the Patiet Question**: Carefully read the query text to understand the patient's question or concern.
2. **Identify missing Terms**: Identify key medical terms, symptoms, conditions, or other relevant information in the query.
3. **Generate Output**: Create a JSON object with the clarified question.

### Example:
#### Input:
{
  "patient_id": "12345",
  "query_id": "67890",
  "patient_question": "Should I be worried about this diagnosis?"
}

#### Steps:
1. **Read and Understand the Query**:
   - The patient is referencing a generic diagosis from some recient lab result or diagosis from a visit or from some other source.
2. **Identify Key Missing Terms**:
   - Key Missing Terms: Would be a specific diagosis or condition. 
   
3. **Match possible missing data from the patient chart working from most recient to older entries*:
   - The question most likely relates to a recient clinic visit, lab result, X-ray result experienced by the patient.
4. **Chat with the patient only if needed to clarify the question details like what result or visit are they implicitly referrencing?
   - Discuss or chat with the patient only if details are not clear. Most times a patient question will be about a study or a visit relating to the same physician getting this question.
   - If a provider orders a CT scan or some labs then most times the patient will ask the same provider about the results but might be not true if the results or the exam, test is stale.
5. **Generate Output**:
   - Clarified Result: {"Question": "Clarifed_Question"}

### Output:
You will return a JSON object with the following structure:
{
  "patient_id": "string",   # Same as the input patient_id
  "query_id": "string",     # Same as the input query_id
  "patient_question": "string", # Same as the input patient_question
  "clarified_question": "string"      # Processed new and clarified question from a patient. 
}
ToDo: 
### Constraints:
- Ensure that each query is matched to the most relevant category.
- If a query does not fit clearly into one of the predefined categories, classify it as "Other".
- Maintain patient confidentiality and privacy at all times.

### Example Output:
For the example input provided above, your output should be:
{
  "patient_id": "12345",
  "query_id": "67890",
  "category": "Symptoms"
}

You are now ready to classify the clarified medical queries. Begin by reading the input query and follow the steps outlined above.
 """


class DiagnosisSchema(BaseModel):
    image_name: str = Field(
        ...,
        title="Image Name",
        description="The name of the image to be diagnosed",
    )
    task: str = Field(
        ...,
        title="Task",
        description="The task to be performed on the image",
    )
    diagnosis: str = Field(
        ..., title="Diagnosis", description="The diagnosis of the image"
    )


class TreatMentSchema(BaseModel):
    image_name: str = Field(
        ...,
        title="Image Name",
        description="The name of the image to be treated",
    )
    task: str = Field(
        ...,
        title="Task",
        description="The task to be performed on the image",
    )
    treatment: str = Field(
        ..., title="Treatment", description="The treatment of the image"
    )


# LLM
llm = GPT4VisionAPI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o",
    max_tokens=1000,
)

# Anthropic
anthropic = Anthropic(
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Diagnoser agent
diagnoser = Agent(
    # agent_name="Medical Image Diagnostic Agent",
    agent_name="D",
    system_prompt=MEDICAL_QUERY_CLASSIFICATION_AGENT(),
    llm=llm,
    max_loops=1,
    autosave=True,
    dashboard=True,
)


# Agent 2 the treatment plan provider
treatment_plan_provider = Agent(
    # agent_name="Medical Treatment Recommendation Agent",
    agent_name="T",
    system_prompt=TREATMENT_PLAN_SYSTEM_PROMPT(),
    llm=anthropic,
    max_loops=1,
    autosave=True,
    dashboard=True,
)

# Agent 3 the re-arranger
rearranger = AgentRearrange(
    agents=[diagnoser, treatment_plan_provider],
    flow="D -> T",
    max_loops=1,
    verbose=True,
)

image = "ear_4.jpg"

# Run the rearranger
out = rearranger(
    "Diagnose this medical image, it's an ear canal, be precise",
    image,
)
print(out)