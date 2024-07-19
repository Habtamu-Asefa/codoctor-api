from codoctor_ai import CoDoctor

codoctor = CoDoctor()

config_1 = {"configurable": {"session_id": "abc1"}}
session_id = "abc1"

if __name__ == "__main__":
    # Define ANSI color codes
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"

    # Print a message
    print(f"{RED}Start of conversation with CoDoctor.\n \n{RESET}")

    while True:
        content = input("You: ")
        response = codoctor.invoke(content=content, session_id=session_id) # Try calling the invoke the ai like this for now
        print(f"{GREEN}{response}{RESET}\n")

