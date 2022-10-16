from flask import Flask, render_template, request
from py4j.java_gateway import JavaGateway


import os
import aiml
from autocorrect import spell

app = Flask(__name__)
gateway = JavaGateway()
maggie = gateway.entry_point.getMaggie()


BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    query = [spell(w) for w in (query.split())]
    question = " ".join(query)
    response = maggie.getResponse(question)
    if response:
        return (str(response))
    else:
        return (str(":)"))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port='5000')


