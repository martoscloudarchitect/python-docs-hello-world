from flask import Flask
from pyspark import SparkContext  
from operator import add 

app = Flask(__name__)

@app.route("/")
def hello():
    s = "Azure ! "
    sc = SparkContext()  
    data = sc.parallelize(list("Hello World"))  
    counts = data.map(lambda x: (x, 1)).reduceByKey(add).sortBy(lambda x: x[1], ascending=False).collect()  
    for (word, count) in counts:  
        s = s + "  ,  " + count 
    sc.stop()
    return s
