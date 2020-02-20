# CTF Project for 50.042 Foundations of Cybersecurity
## Introduction
This project was created for an SUTD group project submission. All instructions can be see inside [CTF_Instructions.pdf](CTF_Instructions.pdf).
The rest of the files here are to run a Django server to assist the students in completing the CTF.
The server serves 2 purpose:
1. Allows students to check their answers
2. Allows students to generate a Rubik's Cube image equivilence of their encoded message to assist them in their CTF process.

For point 2, the program uses [OpenCV](https://pypi.org/project/opencv-python/) to assist in the image generation. Here is one example of an image generated:

![](sample_cube.jpeg)


For more information on how each endpoint works and how the user interacts with the server, see [CTF_Instructions.pdf](CTF_Instructions.pdf).

## How to run server
You can setup a [venv](https://docs.python.org/3/library/venv.html) first if you want.
1. `pip3 install -r requirements`
2. `python3 manage.py runserver`
