from flask import Flask, render_template, Response
from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()

    def events():
        for topic in client.topics[topicname].get_simple_consumer():
            # dont want to return here just make a generator to yield an iterable
            yield 'data:{0}\n\n'.format(topic.value.decode())
        
    return Response(events(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug='True',port=5001)