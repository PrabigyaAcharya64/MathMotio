
def get_user_query():
    print("Welcome to the Manim Animation Generator!")
    print("Describe the animation you want (e.g., 'Show a circle and animate a point moving along its circumference.')")
    user_query = input("Enter your animation description: ")
    return user_query

if __name__ == "__main__":
    query = get_user_query()
    print(f"Received query: {query}")
    
