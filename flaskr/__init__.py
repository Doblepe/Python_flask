from flask import Flask, request, render_template
import pandas as pd
import json
import csv


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')


@app.route("/iris/", methods=["GET"])
def irisData():
    df = pd.read_csv("iris.csv")
    describe = df.describe().to_json(orient="index")
    describe = json.loads(describe)
    return describe

@app.route("/insertData/", methods= ['POST'])
def insertData():
    data = request.data
    data = json.loads(data)
    with open("iris.csv", "a", newline="") as csvFile:
        fieldnames = ['sepal_length','sepal_width','petal_length','petal_width','species']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writerow({'sepal_length': data['sepal_length'],
        'sepal_width': data['sepal_width'],'petal_length':data['petal_length'],
        'petal_width':data['petal_width'],'species':data['species']})
        print('ARchivo completado')
        return data
@app.route("/updateData/", methods=["PUT"])
def updateData():
    data = request.data
    data = json.loads(data)
    df = pd.read_csv('iris.csv')
    df.loc[df.index[-1], "sepal_length"] = data['sepal_length'],
    df.loc[df.index[-1], "sepal_width"] = data['sepal_width'],
    df.loc[df.index[-1], "petal_length"] = data['petal_length'],
    df.loc[df.index[-1], "petal_width"] = data['petal_width'],
    df.loc[df.index[-1], "species"] = data['species']
    df.to_csv("iris.csv", index=False)
    result = df.iloc[-1].to_json(orient="index")
 
    return json.loads(result)
@app.route("/deleteData/", methods=['DELETE'])
def deleteData():
    df = pd.read_csv('iris.csv')
    df.drop(df.index[-1], inplace=True)
    df.to_csv('iris.csv', index=False)
    result = df.iloc[-1].to_json(orient="index")
    return json.loads(result)




if __name__ == "__main__":
    app.run(debug=True)
