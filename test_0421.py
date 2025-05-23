from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

# Load Qwen model and tokenizer
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Event storage (in-memory)
event_data = pd.DataFrame(columns=["ID", "Title", "Start", "End", "Location", "Participants"])

# Helper function for AI response
def get_ai_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to handle user input
def handle_user_input(user_input):
    global event_data

    # Prompt Engineering
    prompt = f"""
    You are an event scheduling assistant. The user input is: "{user_input}"
    Your task is to:
    1. Determine the user's intent (schedule, edit, check, delete).
    2. Extract relevant details such as:
       - Event Title
       - Date and Time (Start and End)
       - Location
       - Participants
    3. Provide the action and extracted details in a structured format as a Python dictionary.

    Examples:
    - Input: "Schedule a meeting on Monday at 9am."
      Output: {{'Action': 'schedule', 'Event Title': 'Meeting', 'Date and Time': {{'Start': 'Monday 9am', 'End': 'Monday 10am'}}, 'Location': 'N/A', 'Participants': 'N/A'}}

    - Input: "Change the meeting on Monday to 10am."
      Output: {{'Action': 'edit', 'Event ID': 1, 'Event Title': 'Meeting', 'Date and Time': {{'Start': 'Monday 10am', 'End': 'Monday 11am'}}, 'Location': 'N/A', 'Participants': 'N/A'}}

    - Input: "What events do I have on Monday?"
      Output: {{'Action': 'check', 'Date': 'Monday'}}

    - Input: "Delete the meeting on Monday at 9am."
      Output: {{'Action': 'delete', 'Event ID': 1}}

    Now process the user's input and provide the output.
    """

    # Get AI response
    response = get_ai_response(prompt)
    print(f"Model Response: {response}")

    # Process the AI response
    try:
        action_details = eval(response)  # Assuming the model outputs a valid Python dictionary
        action = action_details.get("Action")

        if action == "schedule":
            # Add the event
            event_id = len(event_data) + 1
            event_data = event_data.append({
                "ID": event_id,
                "Title": action_details['Event Title'],
                "Start": action_details['Date and Time']['Start'],
                "End": action_details['Date and Time']['End'],
                "Location": action_details.get("Location", "N/A"),
                "Participants": action_details.get("Participants", "N/A")
            }, ignore_index=True)
            print("Event scheduled successfully!")

        elif action == "edit":
            # Edit the event
            event_id = action_details.get("Event ID")
            if event_id in event_data["ID"].values:
                event_data.loc[event_data["ID"] == event_id, ["Title", "Start", "End", "Location", "Participants"]] = [
                    action_details['Event Title'],
                    action_details['Date and Time']['Start'],
                    action_details['Date and Time']['End'],
                    action_details.get("Location", "N/A"),
                    action_details.get("Participants", "N/A")
                ]
                print("Event updated successfully!")
            else:
                print("Event not found!")

        elif action == "check":
            # Check events
            date_filter = action_details.get("Date")
            if date_filter:
                filtered_events = event_data[event_data["Start"].str.contains(date_filter, na=False)]
                print(filtered_events if not filtered_events.empty else "No events found for the given date.")
            else:
                print(event_data if not event_data.empty else "No events scheduled.")

        elif action == "delete":
            # Delete the event
            event_id = action_details.get("Event ID")
            if event_id in event_data["ID"].values:
                event_data = event_data[event_data["ID"] != event_id]
                print("Event deleted successfully!")
            else:
                print("Event not found!")

        else:
            print("Unknown action. Please try again.")
    except Exception as e:
        print("Failed to process model response. Please try again.")
        print(f"Error: {e}")

# Main loop for user interaction
def main():
    print("Welcome to Event Scheduler!")
    while True:
        user_input = input("How can I help you today? (e.g., Schedule a meeting on Monday at 9am): ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        handle_user_input(user_input)

# Run the program
if __name__ == "__main__":
    main()
