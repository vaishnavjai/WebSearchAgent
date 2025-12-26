import ollama

assistant_convo= []

def stream_assistant_response():
    global assistant_convo
    responseStream = ollama.chat(model='llama3.1:8b', messages=assistant_convo, stream=True) #pulling string from ollama chat where stream keeps constantly updating the chat to the response stream
    completeResponse = '' #init complete response
    print('Assistant:')

    for chunk in responseStream:
        print(chunk['message']['content'],end='',flush=true) #flush forces all pending writes to be sent immediately preventing data loss
        completeResponse+=chunk['message']['content']

    assistant_convo.append({'role':'assistant','content': completeResponse})
    print("\n\n")

def main():
    while True:
        prompt = input('USER:\n')
        assistant_convo.append({'role':'user','content':prompt})
        stream_assistant_response()
if __name__ == '__main__':
    main()