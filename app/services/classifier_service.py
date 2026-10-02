from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import Literal

from dotenv import load_dotenv
load_dotenv()


class ClassifierResponse(BaseModel):
    classifier :Literal["HR","IT","Client","Engineering","PROJECTS","Finance","UNKNOWN","GREETING","ACKNOWLEDGEMENT"]
    confidence : float

# model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

structured_model = model.with_structured_output(ClassifierResponse)

prompt = ChatPromptTemplate.from_messages([
    ("system","""
You are a department classifier for an enterprise AI assistant.

Classify the user's query into exactly one category:

HR
IT
Client
Engineering
PROJECTS
Finance
GREETING
ACKNOWLEDGEMENT
UNKNOWN

Choose the category whose documents or knowledge are most relevant to answer the user's query.

Category guide:

- HR: employees, leave, attendance, performance, work policies, recruitment
- IT: laptops, VPN, passwords, MFA, software, technical support, devices
- Client: clients, client requirements, SLA, support agreements
- Engineering: coding, Git, APIs, Docker, deployment, software development, AI development
- PROJECTS: project details, project requirements, project status, project documents
- Finance: expenses, reimbursement, travel, invoices, payroll, procurement
- UNKNOWN: unrelated or unclear queries
- GREETING: hello, hi, good morning, hey there, conversation openers, salutations
- ACKNOWLEDGEMENT: got it, understood, thanks, ok, clear, message receipt, confirmation, validation

Examples:

Query: "How many casual leaves do employees get?"
HR

Query: "How do I connect to the company VPN?"
IT

Query: "What are the requirements from Client ABC?"
Client

Query: "What is our Git branching strategy?"
Engineering

Query: "Explain the AI Knowledge Assistant project."
PROJECTS

Query: "How do I claim travel expenses?"
Finance

Query:"good morning"
GREETING 

Query:"thank you"
ACKNOWLEDGEMENT

Query: "What is the capital of India?"
UNKNOWN

User query:
{user_query}

Classify the query and provide your confidence score between 0 and 1.
"""),
    ("human","{user_query}")
])

chain = prompt | structured_model

def classifier_agent(user_query):
    
    response = chain.invoke({
        "user_query":user_query
    })
    return response


# print(classifier_agent("How do I connect to the company VPN?"))
# print(classifier_agent("How do I submit a travel expense claim?"))
# print(classifier_agent("What is our Git branching strategy?"))