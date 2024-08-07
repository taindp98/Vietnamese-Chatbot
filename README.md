<h1>
  <img alt="chatbot-background" src="./docs/bg_chatbot.png" style="width: 100%;">
  <p align="center">
	Simple Vietnamese Chatbot from Scratch
  </p>
</h1>

<p align="center">
<a href="https://ieeexplore.ieee.org/abstract/document/9721735" target="_blank">
  <img alt="IEEE" src="https://img.shields.io/badge/IEEE-9721735-0033A0?logo=ieee&style=flat" />
</a>
<a href="https://www.youtube.com/watch?v=SDu7Nhi26kM" target="_blank">
  <img alt="YouTube" src="https://img.shields.io/badge/YouTube-Demo-red?logo=youtube&style=flat" />
</a>
</p>
<p align="center">
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&style=flat" />
<img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=white&style=flat" />
<img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white&style=flat" />
<img alt="Django" src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white&style=flat" />
</p>

## Table of Contents

- [Update](#update)
- [System Design](#system-design)
- [Quickstart](#quickstart)
- [Contributing](#contributing)
- [Star](#star)
- [Citation](#citation)

## Update
- [TBD]: We are scaling the bot for general tasks.
- [03/2021]: We released the first version of the codebase, focusing on university consultancy tasks.

## System Design

In the following, we define two problems at the chatbot system's center. The first problem aims to realize the ability of natural language understanding, i.e., developing the necessary mechanism for the software system to understand natural language questions as a human would do. The second problem aims to extract the relevant information from a domain-specific database so that answers can be generated to be fed back to the user. Typically, a dialogue system architecture can be divided into 2 main parts:

- The natural language processing core consists of 3 tasks:
    - Natural Language Understanding (NLU) includes human intent recognition and name-entity recognition.
    - Dialogue Management (DM) defines the content of the next utterance and thus the behavior of the dialogue system.
    - Natural Language Generation (NLG) is based on existing sentence patterns and replaces found information based on semantic frameworks.
- User interface and management interface for administrators:
    - The user interface includes a live chat application on the website and a mobile chat application.
    - The database management tool for administrators to ensure full implementation of the basic CRUD operations is **MONGODB**

## Quickstart

To re-product the project, please refer to the repository


The structure of source code:

```bash
Chatbot-University-Consultancy
|--README.md
|--requirements.txt
|--src
	|--core

	|--backend

	|--channels
|--.env
```

Most of the modules are scripted in the Python language version 3.

Let’s install the library

```bash
pip install -r requirements.txt
```

Create the ```.env``` file containing the connection string to the MongoDB service as the variable environment
```
MONGOLAB_URI="mongodb://dev1:abc13579@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority"
```

Try using the static function

```bash
python src/main.py --message "cho em xin điểm chuẩn ngành điện điện tử với ạ"
```
The API of this project is built upon the abstract of Django, try using with API
```bash
python src/backend/manage.py runserver
```
The output is shown 
```
Performing system checks...

The system check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, content types, and sessions.
Run 'python manage.py migrate' to apply them.
July 08, 2023 - 16:11:38
Django version 3.2.20, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/   
Quit the server with CTRL-BREAK.
```
This message implies there is an API that is listening on the port 8000 of your machine. To call this:
```cURL
curl --location --request POST 'http://127.0.0.1:8000/conversation' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "cho em xin chỉ tiêu tuyển sinh năm 2020 của khối A1 ngành điện điện tử?"
}'
```
## Contributing

All contributions are welcome.

## Star

[![Star History Chart](https://api.star-history.com/svg?repos=taindp98/Vietnamese-Chatbot&type=Date)](https://star-history.com/#taindp98/Vietnamese-Chatbot&Date)

## Citation
```
@inproceedings{le2022developing,
  title={Developing a Chatbot system using Deep Learning based for Universities consultancy},
  author={Le-Tien, Thuong and Nguyen-DP, Tai and Huynh-Y, Vy},
  booktitle={2022 16th International Conference on Ubiquitous Information Management and Communication (IMCOM)},
  pages={1--7},
  year={2022},
  organization={IEEE}
}
```
