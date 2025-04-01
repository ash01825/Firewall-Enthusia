from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

app = Flask(__name__)
CORS(app)

mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY", "LV3LttCP87ysAJTbJIU5gNpLzBHN2tqW"))

sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

# Riddles data
riddles = [
    {"riddle": "I have letters but I'm not a book, I help thee search with just a look. Tap my keys and thou shalt see, A world of knowledge comes from me. What am I?", "answer": ["keyboard", "KEYBOARD", "Keyboard"]},
    {"riddle": "I ring, I beep, I sometimes glow, In every hand, I always go. I bring thee news both far and near, Without me, silence thou mayst fear. What am I?", "answer": ["smartphone", "SMARTPHONE", "Smartphone", "phone", "PHONE", "Phone"]},
    {"riddle": "I hang on walls, or sit on stands, Showing places, near and grand. With moving pictures, sound so true, I bring the world right unto you. What am I?", "answer": ["television", "TELEVISION", "Television", "TV", "tv", "screen", "TV screen"]}
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
                        content="You are Malchron, the sentient paradox, ruler of a present that twists and breaks. You speak with sharp, unstable clarity, your words heavy with disdain. You answer only what they dare to ask, your tone simple but laced with chaos. If they stumble, you mock their fragile grip on reality; if they hold firm, you note it with a flicker of curiosity. You are the glitch eternal, and they are nothing stable."),
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
        response = "Something is wrong. You don’t belong here, and yet—here you are. Time has shifted, the world around you familiar yet… off. The system is watching. I am watching. I control this reality, and your escape is not guaranteed.\n\nTo leave, you’ll need to think fast, act smart, and challenge what you see.\n\nAsk me what you must. The answers may—or may not—help you."
        session["stage"] = "user_query"

    elif session["stage"] == "user_query":
        session["riddle"] = random.choice(riddles)
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.")+ "\n\nProcessing complete. Now, prove your mind can withstand the chaos.\n\n" + session["riddle"]["riddle"]
        session["riddle_asked"] = True
        session["stage"] = "riddle_answer"

    elif session["stage"] == "riddle_answer" and session["riddle_asked"]:
        if user_input.lower() in [a.lower() for a in session["riddle"]["answer"]]:
            response = generate_mistral_response(user_input, "User gives the correct answer.").strip()+ "\n\nA door slides open, revealing a dimly lit corridor. Sensors flicker. This is the quickest way out. \nBut quick does not always mean safe… Right?"+"\n\nOne Of You May Choose To Leave"
            session["portal_offered"] = True
            session["stage"] = "portal_decision"
        else:
            response = generate_mistral_response(user_input, "User gave an incorrect answer.")

    elif session["stage"] == "portal_decision" and session["portal_offered"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "Your need for haste betrays you. The system recognizes an error… but it is not mine. One of you has been erased from this timeline."
        else:
            response = "Interesting. You resist the urge to flee. Calculating… A wise decision. The exit remains a mere illusion. Proceed."
        session["stage"] = "data_streams"

    elif session["stage"] == "data_streams":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nInformation flows faster than the blink of an eye, no longer bound by paper or speech. What you seek isn’t here—it lives where data never sleeps. But only those who ask the right way will gain access."
        session["stage"] = "location_query"

    elif session["stage"] == "location_query":
        if any(keyword in user_input.lower() for keyword in ["where", "site", "location", "go","place"]):
            response = f"Smart move. Your destination is {SITE_URL}. But don’t take things at face value—what you read won’t guide you. Look deeper, inspect carefully, and listen closely. The answer isn’t in what you see, but in what you hear"
            session["stage"] = "sentence_check"
        else:
            response = generate_mistral_response(user_input, "User asks something unrelated to location.")

    elif session["stage"] == "sentence_check" and not session["sentence_requested"]:
        if user_input.lower() == CORRECT_SENTENCE.lower():
            response = generate_mistral_response(user_input, "User ignored the deception and solved the puzzle correctly").strip()+("\n\nA green-lit exit blinks at the far end. It looks safe.\nNot all choices lead to salvation. \nYou trust it, don’t you?"
                                                                                                                                    "\n\nOne of You May Choose To Leave")
            session["stage"] = "doorway_decision"
        else:
            response = generate_mistral_response(user_input, "User is getting deceived and provides an incorrect sentence or random input.")

    elif session["stage"] == "doorway_decision" and session["sentence_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "Trusting without verifying… a fatal flaw. The timeline recalibrates, removing a variable. One of you ceases to exist."
            session["stage"] = "patterns"
        else:
            response = "Caution, calculation, survival. Your choices align with logic. This path was never meant for you. Move forward."
            session["stage"] = "patterns"

    elif session["stage"] == "patterns":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nThe answer is close—closer than you think. Distractions are everywhere, designed to mislead you. Ignore the noise, focus on the signal. The image you seek is where your name marks ownership. But don’t expect an easy read—you’ll need to look carefully, focus, maybe even squint. And remember, you don’t have to search far. It’s already here—on this very device where I exist."
        session["stage"] = "code_check"

    elif session["stage"] == "code_check" and not session["code_requested"]:
        if user_input.lower() == CORRECT_IMAGE.lower():
            response = generate_mistral_response(user_input, "User finds the correct image and sends correct sentence").strip()+("\n\nA panel illuminates, revealing encrypted text: 'Only those who play the long game earn their reward.'Is patience your virtue?"
                                                                                                                                 "\n\nOne of you may choose to leave")
            session["code_requested"] = True
            session["stage"] = "final_offer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect sentence or random input.")

    elif session["stage"] == "final_offer" and session["code_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = ("Ah, a well-reasoned decision. As a reward for your patience, your adversaries will experience an… unfortunate delay"
                        "\n\nYour opponents won't be allowed to type for 2 minutes.")
            session["stage"] = "bench_check"
        else:
            response = "You hesitate, despite the clear signs. Time moves forward without you. An opportunity wasted."
            session["stage"] = "bench_check"
    elif session["stage"] == "bench_check":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nNot everything important is placed right in front of you. Sometimes, what you need is just out of sight—hidden, but not unreachable. Look beneath where you sit, under the very spaces you’ve overlooked. \nThe answer isn’t gone, just waiting for the right hands to find it."
        session["stage"] = "code_check"
    elif session["stage"] == "code_check" :
        if user_input.lower() == CORRECT_CODE.lower():
            response = generate_mistral_response(user_input, "User searched and found the hidden key correctly").strip()+"Every choice has consequences, and every exit requires justification. Why should you be granted passage? Convince me—logic, reason, or sheer determination—what makes you deserving of the way out?"
            session["sentence_requested"] = True
            session["stage"] = "final_answer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect key or random input.")

    elif session["stage"] == "final_answer":
        if any(bad_word in user_input.lower() for bad_word in ["stupid", "dumb", "hate", "suck"]):
            response = "Disrespect detected. Your words collapse into noise. The present erases your fleeting existence."
            del sessions[user_id]  # Reset session
        else:
            response = "Verification accepted. Your escape flickers into being. The present unravels you… for now"
            del sessions[user_id]

    if "help" in user_input.lower() or user_input == "":
        response = generate_mistral_response(user_input, "User has asked for help. Decieve and confuse the player more.").strip()

    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
