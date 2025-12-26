import ollama
from searchOrNot import search_or_not_msg
import re

assistant_convo= []
def searchOrNot():
    sys_msg = search_or_not_msg
    response = ollama.chat(model='llama3.1:8b',
                           messages=[{'role' : 'system', 'content': sys_msg} , assistant_convo[-1]] 
                           )
    print(f"Search or not Response: {response['message']['content'].strip()}")
    if 'true' in response['message']['content'].lower():
        return True
    else:
        return False
    
def stream_assistant_response():
    global assistant_convo
    responseStream = ollama.chat(model='llama3.1:8b', messages=assistant_convo, stream=True) #pulling string from ollama chat where stream keeps constantly updating the chat to the response stream
    completeResponse = '' #init complete response
    print('Assistant:')

    for chunk in responseStream:
        print(chunk['message']['content'],end='',flush=True) #flush forces all pending writes to be sent immediately preventing data loss
        completeResponse+=chunk['message']['content']

    assistant_convo.append({'role':'assistant','content': completeResponse})
    print("\n\n")

def main():
    while True:
        prompt = input('USER:\n')
        assistant_convo.append({'role':'user','content':prompt})
        if searchOrNot():
            print("Searching the web for more data...\n")
            # Here you would implement the actual search logic and append the results to assistant_convo
        stream_assistant_response()
if __name__ == '__main__':
    main()