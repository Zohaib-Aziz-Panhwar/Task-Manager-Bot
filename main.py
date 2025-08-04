import pymongo
import datetime
import google.generativeai as genai

genai.configure(api_key="AIzaSyBYuTr9gknOcuA9VOvnNLxbrvotajvPSs0")  
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat()


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task_db"]
task_collection = db["tasks"]


def insert_task(task_name, due_date_str):
    try:
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
        task = {"task_name": task_name, "due_date": due_date}
        result = task_collection.insert_one(task)
        return " Task added!"
    except Exception as e:
        return f" Failed to add task: {e}"

def delete_task_by_name(task_name):
    result = task_collection.delete_one({"task_name": task_name})
    if result.deleted_count:
        return f" Task '{task_name}' deleted."
    return f" Task '{task_name}' not found."

def get_all_tasks():
    tasks = list(task_collection.find())
    if not tasks:
        return " No tasks found."
    return "\n".join([f" {task['task_name']} | Due: {task['due_date'].strftime('%Y-%m-%d')}" for task in tasks])

def chat_with_bot(user_input):
    try:
        if not user_input.strip():
            return "Please type something."

        lower_input = user_input.lower().strip()

        if "show" in lower_input and "task" in lower_input:
            return get_all_tasks()

        elif "delete task" in lower_input:
            task_name = user_input.split("delete task", 1)[1].strip()
            return delete_task_by_name(task_name)
        
        elif lower_input.startswith("add task"):
            try:
                parts = user_input[8:].strip().rsplit(" ", 1)
                task_name = parts[0]
                due_date = parts[1]
                return insert_task(task_name, due_date)
            except Exception as e:
                return " Format: add task <task name> <YYYY-MM-DD>"

        response = chat.send_message(user_input)
        return response.text.strip()

    except Exception as e:
        return f" Chatbot error: {e}"


def chat_bot_interface():
    print(" Chatbot Mode (type 'exit' to return)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Returning to menu...")
            break
        response = chat_with_bot(user_input)
        print("Bot:", response)

def menu():
    print("\n📋 MENU:")
    print("1. Add task manually")
    print("2. View all tasks")
    print("3. Delete a task")
    print("4. Chat with bot")
    print("5. Exit")

def manual_add_task():
    task_name = input("Enter task name: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    print(insert_task(task_name, due_date))

def manual_view_tasks():
    print(get_all_tasks())

def manual_delete_task():
    task_name = input("Enter task name to delete: ")
    print(delete_task_by_name(task_name))

def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            manual_add_task()
        elif choice == '2':
            manual_view_tasks()
        elif choice == '3':
            manual_delete_task()
        elif choice == '4':
            chat_bot_interface()
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
