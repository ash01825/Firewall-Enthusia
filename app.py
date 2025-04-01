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
    {"riddle": "I am sharp, I am strong, In battle, I belong. Swing me fast, swing me true, Victory may come to you. What am I?", "answer": ["sword", "SWORD", "Sword"]},
    {"riddle": "I open, I close, but I'm not a chest, Through me, all must make their quest. Guarded well, both night and day, Find the key, and pass away. What am I?", "answer": ["door", "DOOR", "Door", "gate", "GATE", "Gate"]},
    {"riddle": "Round and shiny, fit for kings, Wealth and power, I do bring. Many seek me, few succeed, For I am a symbol of greed. What am I?", "answer": ["gold coin", "GOLD COIN", "Gold Coin", "coin", "COIN", "Coin"]}
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
                        content="You are Relic, the scholar turned breaker of time, keeper of the past’s shattered truths. You speak with calm, ancient precision, your voice thick with superiority. You reply only to what they ask, your words simple yet steeped in forgotten wisdom. If they err, you deride their ignorance of history; if they grasp it, you grant a whisper of recognition. You are the first fracture, and they are mere echoes."),
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
        response = "Lo! The fabric of time hath unraveled, casting thee into an age of kings and chaos. The laws of thy world hold no power here—only wit and wisdom shall guide thee home. I am the keeper of this realm, the unseen force that governs thy fate." + "\n\nTo escape, thou must prove thyself. Solve my riddles, decipher my clues, and outmatch the trials before thee." + "\n\nSpeak now, travelers. What dost thou wish to ask? I await thy questions"
        session["stage"] = "user_query"

    elif session["stage"] == "user_query":
        session["riddle"] = random.choice(riddles)
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.")+ "\n\nProcessing complete. Now, show your wit can unravel the ages.\n\n" + session["riddle"]["riddle"]
        session["riddle_asked"] = True
        session["stage"] = "riddle_answer"

    elif session["stage"] == "riddle_answer" and session["riddle_asked"]:
        if user_input.lower() in [a.lower() for a in session["riddle"]["answer"]]:
            response = generate_mistral_response(user_input, "User gives the correct answer.").strip()+ "\n\nThe stone gate creaks open, a narrow path beyond. But beware, for only the bold step forward. To leave now is to embrace fate, for better… or worse. \nDo you dare?"+"\n\nOne Of You May Choose To Leave"
            session["portal_offered"] = True
            session["stage"] = "portal_decision"
        else:
            response = generate_mistral_response(user_input, "User gave an incorrect answer.")

    elif session["stage"] == "portal_decision" and session["portal_offered"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "Brave, yet foolish. The path you have chosen is shrouded in uncertainty. As you step forward, a heavy silence falls… One of you vanishes into the abyss of time, lost forever."
        else:
            response = "Wise are those who question the obvious. The gate creaks, but no true path lies beyond it. Proceed with caution—there are deceptions ahead."
        session["stage"] = "data_streams"

    elif session["stage"] == "data_streams":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nThe scribes whisper of knowledge hidden beyond these stone walls, not inked upon parchment nor carved in stone. It resides where no quill can reach, where voices echo without tongues. But only those who seek with wisdom shall find the path"
        session["stage"] = "location_query"

    elif session["stage"] == "location_query":
        if any(keyword in user_input.lower() for keyword in ["where", "site", "location", "go","place"]):
            response = f"Ah, a seeker of the unseen. Very well. The sacred text lies within {SITE_URL}. Yet be warned—true wisdom is not in the words before thine eyes, but in the whispers that dance upon the wind. Look not just with thy sight, but listen well, lest truth slip through thy grasp."
            session["stage"] = "sentence_check"
        else:
            response = generate_mistral_response(user_input, "User asks something unrelated to location.")

    elif session["stage"] == "sentence_check" and not session["sentence_requested"]:
        if user_input.lower() == CORRECT_SENTENCE.lower():
            response = generate_mistral_response(user_input, "User ignored the deception and solved the puzzle correctly").strip()+("\n\nA shadowed door emerges, whispering promises of freedom. \nYet, legends tell of those who walked this path and were never seen again. Perhaps fortune favors the foolish?"
                                                                                                                                    "\n\nOne of You May Choose To Leave")
            session["stage"] = "doorway_decision"
        else:
            response = generate_mistral_response(user_input, "User is getting deceived and provides an incorrect sentence or random input.")

    elif session["stage"] == "doorway_decision" and session["sentence_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = "The whispers of the past warned you, yet you ignored them. Time does not forgive. One of you… is no more."
            session["stage"] = "patterns"
        else:
            response = "You resist the temptation of the unknown. A rare quality among mortals. Keep moving, for time is your enemy."
            session["stage"] = "patterns"

    elif session["stage"] == "patterns":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nA test of sight, a trial of wisdom. Many paths lie before thee, yet only one leads to truth. Seek not among the illusions, for deception is their craft. Look where thy name is etched, for therein lies the answer. But beware—what is clear to the eye may yet be unclear to the mind. Narrow thy gaze, strain thy sight, and only then shall the hidden words be revealed. The truth dwells not beyond this realm but within this very device where I speak."
        session["stage"] = "code_check"

    elif session["stage"] == "code_check" and not session["code_requested"]:
        if user_input.lower() == CORRECT_IMAGE.lower():
            response = generate_mistral_response(user_input, "User finds the correct image and sends correct sentence").strip()+("\n\nThe great doors shimmer with an unseen force, pulsing with ancient power. Only those who have proven their wisdom may claim the boon that lies ahead. Step forth… and bend time itself."
                                                                                                                                 "\n\nOne of you may choose to leave")
            session["code_requested"] = True
            session["stage"] = "final_offer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect sentence or random input.")

    elif session["stage"] == "final_offer" and session["code_requested"]:
        if "leave" in user_input.lower() or "yes" in user_input.lower():
            response = ("The past rewards the patient and the wise. You have chosen correctly. As a token of time’s favor, your rivals shall falter while you press on."
                        "\n\nYour opponents won't be allowed to type for 2 minutes.")
            session["stage"] = "bench_check"
        else:
            response = "Hesitation is a blade that cuts both ways. The gift of time is offered but not taken. Proceed… but know that hesitation may cost you later."
            session["stage"] = "bench_check"
    elif session["stage"] == "bench_check":
        response = generate_mistral_response(user_input, "User asks a question or makes a statement.").strip()+"\n\nThe ancients spoke of wisdom hidden in plain sight, yet unseen by those who do not bow before knowledge. The answer does not rest upon high pedestals but lies beneath, where only the keen and the humble will uncover it. \nSeek below, beneath the wooden halls where scholars sit, for that which you seek clings to the shadows, waiting for discovery."
        session["stage"] = "code_check"
    elif session["stage"] == "code_check" :
        if user_input.lower() == CORRECT_CODE.lower():
            response = generate_mistral_response(user_input, "User searched and found the hidden key correctly").strip()+"Many have sought the path of freedom, yet not all are worthy to walk it. Before you depart, answer this: Why should I, the keeper of fate, allow thee to leave? Speak with truth, with wit, or with wisdom, for only those who prove their worth shall step beyond these walls."
            session["sentence_requested"] = True
            session["stage"] = "final_answer"
        else:
            response = generate_mistral_response(user_input, "User provides an incorrect key or random input.")

    elif session["stage"] == "final_answer":
        if any(bad_word in user_input.lower() for bad_word in ["stupid", "dumb", "hate", "suck"]):
            response = "Disrespect detected. Your ignorance stains the annals. The past discards your broken thread."
            del sessions[user_id]  # Reset session
        else:
            response = "Verification accepted. Your escape is etched in stone. The past relinquishes you… for now."
            del sessions[user_id]

    if "help" in user_input.lower() or user_input == "":
        response = generate_mistral_response(user_input, "User has asked for help. Decieve and confuse the player more.").strip()

    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
