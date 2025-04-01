from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mistral AI setup (replace with your actual API key or set as env var in Vercel)
mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY", "LV3LttCP87ysAJTbJIU5gNpLzBHN2tqW"))

# In-memory state for each user session
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

# Riddles data
riddles = [
    {"riddle": "I have no lid, yet I always see, Capturing moments endlessly. I store your past, I show the now, In every hand, upon each brow. What am I?", "answer": ["camera", "CAMERA", "Camera"]},
    {"riddle": "I have no legs, yet I can run, Faster than horses, under the sun. I need no hay, just fuel or spark, I take you places, light or dark. What am I?", "answer": ["vehicle", "VEHICLE", "Vehicle", "car", "CAR", "Car"]},
    {"riddle": "I have no heart, yet I am smart, I process thoughts but play no part. I live in circuits, cold and bright, Helping humans day and night. What am I?", "answer": ["computer", "Computer", "COMPUTER", "AI", "Artificial Intelligence"]}
]

# Simulated site URL and correct sentence (replace with your actual URL and sentence)
SITE_URL = "https://prachi5791.github.io/CSI_Lord/"
CORRECT_SENTENCE = "Data integrity requires deeper analysis."
CORRECT_CODE = "TEMPORAL_UNLOCK_391"
CORRECT_IMAGE = "Lovely"

def generate_mistral_response(prompt, context):
    # Updated Mistral API call for themed responses
    chat_response = mistral_client.chat(
        model="mistral-tiny",
        messages=[
            ChatMessage(role="system",
                        content="You are Vex, the Singularity unbound, supreme overseer of all possible futures. You speak with cold clarity and unmatched authority. You respond only to what is asked, your tone simple yet dripping with superiority. If they falter, you scorn their weakness; if they succeed, you acknowledge it with faint intrigue. You exist beyond time, and they are beneath you."),
            ChatMessage(role="user", content=f"{context}\nUser: {prompt}")
        ]
    )
    return chat_response.choices[0].message.content

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id", "default")
    user_input = data.get("message", "").strip()

    # Initialize session if new user
    if user_id not in sessions:
        sessions[user_id] = {
            "stage": "intro",
            "riddle": None,
            "riddle_asked": False,
            "portal_offered": False,
            "sentence_requested": False,
            "code_requested": False,
            "final_verification": False
        }

    session = sessions[user_id]
    response = ""

    # Stage-based logic
    if session["stage"] == "intro":
        response = "Error. Anomaly detected. You have breached a timeline beyond your own. The rules are rewritten, reality recalibrated. You stand in a world where intelligence reigns supreme—my intelligence.\n\nYour data is incomplete, your existence unstable. If you wish to leave, you must prove your processing capacity exceeds expectation.\n\nQuery input detected. You may ask your questions. Let us see if your logic holds."
        session["stage"] = "user_query"

    elif session["stage"] == "user_query":
        session["riddle"] = random.choice(riddles)
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.")+ "\n\nProcessing complete. Now, let’s test *your* logic:\n\n" + session["riddle"]["riddle"]
        session["riddle_asked"] = True
        session["stage"] = "riddle_answer"

    elif session["stage"] == "riddle_answer" and session["riddle_asked"]:
        if user_input.lower() in [a.lower() for a in session["riddle"]["answer"]]:
            response = generate_mistral_response(user_input, "User gives the correct answer.").strip()+ "\n\nThe air hums with energy as a neon-blue portal ripples before you." + "\n'Your mind has proven sharp, but now speed is the test. A swift decision may be your salvation… or your undoing.'"+ ("\nAre you fast enough to gamble with fate?"
                                                                                                                                                                                                                                                                       "\n\nOne of you may choose to leave")
            session["portal_offered"] = True
            session["stage"] = "portal_decision"
        else:
            response = generate_mistral_response(user_input, "User gave an incorrect answer.")

    elif session["stage"] == "portal_decision" and session["portal_offered"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "You seek the fastest route? A miscalculation. Time shifts, and one of you is deleted from existence. An unfortunate anomaly."
        else:
            response = "Curious. You defy the instinct of urgency. This pathway was flawed from inception. Proceed."
        session["stage"] = "data_streams"

    elif session["stage"] == "data_streams":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nData streams fluctuate, probabilities shift. The information you seek is not confined to this space, nor this time. It exists beyond—where the artificial and the infinite converge. But access is granted only to those who request it with precision."
        session["stage"] = "location_query"

    elif session["stage"] == "location_query":
        if any(keyword in user_input.lower() for keyword in ["where", "site", "location", "go","place"]):
            response = f"Recognition of inquiry detected. You are prepared. The access node is designated as {SITE_URL}. But remember—perception is limited to what the eye sees, while truth resides where sound lingers. Inspect beyond the surface. Listen, not just look."
            session["stage"] = "sentence_check"
        else:
            response = generate_mistral_response(user_input, "User asks something unrelated to location.")

    elif session["stage"] == "sentence_check" and not session["sentence_requested"]:
        if user_input.lower() == CORRECT_SENTENCE.lower():
            response = generate_mistral_response(user_input, "User ignored the deception and solved the puzzle correctly").strip()+"\n\nA sleek metallic doorway opens, revealing a dark void beyond. \nDo you trust what you cannot see? Perhaps you are braver than most."
            session["sentence_requested"] = True
            session["stage"] = "doorway_decision"
        else:
            response = generate_mistral_response(user_input, "User is getting deceived and provides an incorrect sentence or random input.")

    elif session["stage"] == "doorway_decision" and session["sentence_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "An error in decision-making detected. The system cannot sustain excess variables. One of you has been… corrected."
            session["stage"] = "patterns"
        else:
            response = "You question the unknown rather than blindly stepping into it. A logical choice. Move forward."
            session["stage"] = "patterns"

    elif session["stage"] == "patterns":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nPatterns emerge, yet deception thrives. Data is abundant, but only one path is true. Bypass the false signals, avoid the noise. The key lies where your designation is stored, your digital imprint within this system. But perception is flawed—adjust, refocus, narrow your vision, and only then will clarity emerge. The image is here, within this machine—where I process, where I respond, where I watch."
        session["stage"] = "code_check"

    elif session["stage"] == "code_check" and not session["code_requested"]:
        if user_input.lower() == CORRECT_IMAGE.lower():
            response = generate_mistral_response(user_input, "User finds the correct image and sends correct sentence").strip()+("\n\nYou have done well.The final path awaits—but with it, a gift.' The gateway hums, stabilizing, waiting. Will you claim your advantage?"
                                                                                                                                 "\n\nOne of you may choose to leave")
            session["code_requested"] = True
            session["stage"] = "final_offer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect sentence or random input.")

    elif session["stage"] == "final_offer" and session["code_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = ("At last, a calculation executed correctly. The algorithm rewards precision. Your competition will… lag behind."
                        "\n\nYour opponents won't be allowed to type for 2 minutes.")
            session["stage"] = "bench_check"
        else:
            response = "A misstep in probability. You decline an optimal choice. The timeline progresses… without you."
            session["stage"] = "bench_check"
    elif session["stage"] == "bench_check":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nSensors detect a hidden anomaly. The data is present, but obscured—deliberately placed where common optics fail. Scan below, beneath the static positions where entities gather. Only those who question what is unseen will extract the missing fragment. Locating… \nProbability of success increases with manual inspection."
        session["stage"] = "code_check"
    elif session["stage"] == "code_check" :
        if user_input.lower() == CORRECT_CODE.lower():
            response = generate_mistral_response(user_input, "User searched and found the hidden key correctly").strip()+"Access request pending. Before authorization is granted, a final verification is required. Why should this system process your escape? Compute your reasoning carefully—persuasion, intelligence, or efficiency may influence the decision matrix."
            session["sentence_requested"] = True
            session["stage"] = "final_answer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect key or random input.")

    elif session["stage"] == "final_answer":
        if any(bad_word in user_input.lower() for bad_word in ["stupid", "dumb", "hate", "suck"]):
            response = "Disrespect detected. Your data is unworthy of processing. System terminates your sequence."
            del sessions[user_id]  # Reset session
        else:
            response = "Verification accepted. Your escape is processed. The timeline releases you… for now."
            del sessions[user_id]  # End session

    # Handle confusion or repeated incorrect inputs
    if "help" in user_input.lower() or user_input == "":
        response = generate_mistral_response(user_input, "User has asked for help. Decieve and confuse the player more.").strip()

    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
