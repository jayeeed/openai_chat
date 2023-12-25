import requests
import json
from datetime import datetime

SERVER_ENDPOINT = "http://127.0.0.1:5000/api/chat"

# Initialize a session object to store the conversation history
session = requests.Session()
conversation = []  # Local storage for the conversation
user_name = "You"

def chat():
    print("-" * 40)
    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit", "bye", "sys", "oggy"]:
                print("\nExiting the conversation. Goodbye!")
                break

            # Append the user's input to the local conversation history
            conversation.append({"role": "user", "content": user_input})

            try:
                # Send the user's input to the server, including the hardcoded user name
                response = session.post(SERVER_ENDPOINT, 
                                        json={
                                            "input": user_input, 
                                            "user_name": user_name
                                            }, 
                                            timeout=10)
                
                response.raise_for_status()
                
                chatbot_response = response.json()["response"]

                # Append the assistant's response to the local conversation history
                conversation.append({"role": "assistant", "content": chatbot_response})
                
                print("-" * 40)
                print("Oggy:", chatbot_response)
                print("-" * 40)

            except requests.exceptions.HTTPError as http_err:
                # Handle HTTP errors
                print(f"HTTP error occurred: {http_err}")

            except requests.exceptions.ConnectionError:
                # Handle errors like the server being down
                print("Error: Could not connect to the server. Please check if the server is running.")

            except requests.exceptions.Timeout:
                # Handle the server taking too long to respond
                print("Timeout error: The server is taking too long to respond. Please try again later.")

            except requests.exceptions.RequestException as e:
                # Handle any other requests exceptions
                print(f"An error occurred: {e}")

    except KeyboardInterrupt:
        print("\nConversation interrupted by user.")

    finally:
        save_conversation()

def save_conversation():
    # Save conversation to local file
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_conversation_{user_name}.json"
    
    with open(filename, "w") as json_file:
        json.dump(conversation, json_file, indent=4)
        print(f"Conversation saved locally to {filename}")

    try:
        # Request the server to save the conversation, including the hardcoded user name
        response = session.post("http://127.0.0.1:5000/api/chat/end", 
                                json={
                                    "conversation": conversation, 
                                    "user_name": user_name
                                    }, 
                                    timeout=10)
        
        response.raise_for_status()
        print("Conversation saved on the server side.")

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError:
        # Handle errors like the server being down
        print("Error: Could not connect to the server. Please check if the server is running.")

    except requests.exceptions.Timeout:
        # Handle the server taking too long to respond
        print("Timeout error: The server is taking too long to respond. Please try again later.")

    except requests.exceptions.RequestException as e:
        # Handle any other requests exceptions
        print(f"Failed to save conversation on the server side.\nError: {e}")

if __name__ == "__main__":
    chat()
