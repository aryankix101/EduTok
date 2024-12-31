import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')

client_llm = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
#print(client_llm.models.list())

client = chromadb.PersistentClient(path="./chroma_db")

# Load the collection
collection = client.get_collection("manim_docs")
print("Collection loaded successfully!")

results = collection.query(
    query_texts=["Teach how to use the binary search algorithm to efficiently find a target value in a sorted array, with step-by-step examples, Python code implementation, and complexity analysis."],
    n_results=5
)

# Print the results

combined_documents = ""
for i, doc in enumerate(results['documents'], start=1):
    doc_content = "\n".join(doc)
    combined_documents += f"\n--- Document {i} ---\n{doc_content}\n"

#print(combined_documents)

#for result in results['documents']:
    #print("Matching Document:", result)


script = "Introduction Scene (5 seconds): Text: 'Welcome to Binary Search' (large font, center screen). Animation: Text appears with a Write effect. Subtitle: 'A powerful algorithm for searching sorted arrays' (smaller font, below main text). Animation: Subtitle fades in below the title. Duration: 2 seconds for the animations, 3 seconds of pause. Transition: Both texts fade out simultaneously. What is Binary Search? (10 seconds): Title: 'What is Binary Search?' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Example Array: '[3, 7, 10, 15, 19, 23, 27]' (displayed horizontally on the screen). Animation: Array values are written out one by one in sequence. Duration: 2 seconds. First Pass: Highlight the entire array. Show 'low' pointer at index 0 with a downward arrow, 'high' pointer at index 6 with a downward arrow, and calculate 'mid' at index 3. Animation: Highlight the value at index 3 (15) in a different color. Display the text: 'Value at mid = 15'. Animation: Fade out the left half ([3, 7, 10]) to indicate it is eliminated. Move the 'low' pointer to index 4. Duration: 3 seconds. Second Pass: Highlight the new array ([19, 23, 27]). Show 'low' pointer at index 4 and 'high' pointer at index 6. Calculate 'mid' at index 5. Animation: Highlight the value at index 5 (23) in a different color. Display the text: 'Value at mid = 23'. Animation: Fade out the right half ([23, 27]) to indicate it is eliminated. Move the 'high' pointer to index 4. Duration: 3 seconds. Third Pass: Highlight the final value ([19]). Show both 'low' and 'high' pointers at index 4. Calculate 'mid' at index 4. Animation: Highlight the value at index 4 (19) in a different color. Display the text: 'Value at mid = 19. Target found!'. Duration: 2 seconds. Code Walkthrough (15 seconds): Title: 'Python Code Implementation' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Code: Display Python code for binary search line by line, as if being typed out. Animation: Highlight key sections (e.g., while loop, if conditions, and return statements) as they are explained. Duration: 10 seconds for the code walkthrough, including pauses for highlights. Fade out code at the end. Time and Space Complexity (15 seconds): Title: 'Complexity Analysis' (large font, center screen). Animation: Title appears with a Write effect, stays on screen for 2 seconds, then fades out. Display: 'Time Complexity: O(log n)' and 'Space Complexity: O(1)' (stacked vertically, center screen). Animation: Each line appears with a FadeIn effect. Duration: 3 seconds for the animation, 12 seconds of pause for explanation. Fade out both lines at the end. Conclusion Scene (10 seconds): Text: 'Binary Search is simple yet elegant.' (large font, center screen). Animation: Text appears with a Write effect. Subtitle: 'Use it to save time and resources!' (smaller font, below main text). Animation: Subtitle fades in below the title. Duration: 3 seconds for the animations, 7 seconds of pause. Transition: Both texts fade out simultaneously."

final_str = script + " " + "Documents: " + combined_documents


response = client_llm.chat.completions.create(
    model="deepseek-coder",
    messages=[
        {"role": "system", "content": "You are a helpful assistant who responds with Manim Code file or files to a script for a short (<1 minute) video. You will be provided with the detailed script and documents to assist you in generating the code. Generate the animations exactly how the script details. Complete, correct manim code files are the only thing you should output. Make sure the animations generated visually make sense corresponding to the script and do not overlap and actually run."},
        {"role": "user", "content": final_str},
  ],
    max_tokens=2048,
    temperature=0.7,
    stream=False
)

print(response.choices[0].message.content)
