# Chatbot University Consultancy

Key Skills: Natural Language Processing, System Design

# Developing a Chatbot system using Deep Learning-based for Universities consultancy

Inspired by the recent successes of deep learning in Natural Language Processing(NLP), we propose a chatbot system using Deep Learning for Vietnamese Universities consultancy. 

[https://www.youtube.com/watch?v=SDu7Nhi26kM](https://www.youtube.com/watch?v=SDu7Nhi26kM)

## System Design

In the following, we define two problems that are at the center of the chatbot system. The first problem aims to realize the ability of natural language understanding, i.e., developing the necessary mechanism for the software system to understand natural language questions as a human would do. The second problem aims to extract the relevant information from a domain-specific database so that answers can be generated to be fed back to the user. Typically, a dialogue system architecture can be divided into 2 main parts:

- The natural language processing core consists of 3 tasks:
    - Natural Language Understanding (NLU) includes human intent recognition and name-entity recognition.
    - Dialogue Management (DM) defines the content of the next utterance and thus the behavior of the dialogue system.
    - Natural Language Generation (NLG) is based on existing sentence patterns and replaces found information based on semantic frameworks.
- User interface and management interface for administrators:
    - The user interface includes a live chat application on the website and a mobile chat application.
    - The database management tool for administrators to ensure full implementation of the basic CRUD operations.
        
        ![Untitled](Chatbot%20University%20Consultancy%20e71cb879364d4e4590389410e79b1b90/Untitled.png)
        

## **Quickstart**

To re-product the project, please refer to the repository

[https://github.com/taindp98/Chatbot-University-Consultancy](https://github.com/taindp98/Chatbot-University-Consultancy)

The structure of source code:

```bash
Chatbot-University-Consultancy
|--README.md
|--requirements.txt
|--src
		|--core
				|--nlu
				|--dm
				|--nlg
		|--channels
				|--web
				|--
```

Most of the modules are scripted in the Python language version 3, which is the pre-requisition.

Let’s install the library

```bash
$pip install -r requirements.txt
```