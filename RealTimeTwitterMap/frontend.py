from flask import Flask, jsonify, request, Response, render_template
from pykafka import KafkaClient
import json

#link kafka client again

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

#spin up a new Flask app
app = Flask(__name__)

# flask route to a page, its the page that we see in the browser
# we can define route as, for eg., ("Home"), then we have to add Home to
# the website name/localhost name to see the returns. But since we are defining
# it as an index, its the main page, so we wont change it for now.
@app.route("/")
def index():
# returns anything written inside bracket, even basic "strings"
    return render_template('index.html')

# now we make an actual kafka consumer
# we route the data from the topic and use <topicname>, since <> says its a
# variable. the get_messages takes the variable topicname by itself.

@app.route('/topic/''<topicname>')
def get_messages(topicname):
#calls the function of kafka client, gets kafka broker and stores it in
# client variable
    client = get_kafka_client()

# new function within function.
# complicated
# we open a get_simple_consumer, define i from topics under topicname,
## the topicname is taken dynamically from previous function which in itself
#### takes it from the approute above.
# we have to make a loop to return something, but if we return i,
## the loop will stop after taking taking just one message from KafkaClient.
# so the consumer must be kept alive as newer messages will keep streaming in.
# so we must use a generator, ie,'yield',its a return, but keeps function alive.
# yield i.value is enough, but kafka uses byte format, hence we decode it, so,
## yield.i.value.decode() is good. But we can beautify the data by using,
#### 'data{0}\n\n'.format(i.value.decode())
# finally get_messages need a return. so we return a Response within which we,
## hand it events function, and specify the type of return, which is an
#### event-stream as text.

    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return (Response(events(), mimetype="text/event-stream"))

if __name__ == "__main__":
#keeping debug as true is really powerful since it can change the page
# in just one reload, if the code here is changed
    app.run(debug=True, port=5001)
