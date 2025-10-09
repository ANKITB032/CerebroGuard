import pickle
import networkx as nx
import spacy
from flask import Flask, request, jsonify, render_template # MODIFIED LINE

# --- Configuration ---
graph_file = 'enron_graph.gpickle'

# --- Initialization ---
print("Loading the communication graph...")
with open(graph_file, 'rb') as f:
    G = pickle.load(f)
print("Graph loaded successfully.")

print("Loading NLP model...")
nlp = spacy.load('en_core_web_sm')
print("NLP model loaded successfully.")


# --- Create the Flask App ---
app = Flask(__name__)


# NEW ROUTE TO SERVE THE HTML PAGE
@app.route('/')
def home():
    return render_template('index.html')


def analyze_email(sender, recipient, body):
    """The core analysis engine for CerebroGuard."""
    
    evidence_factors = []
    risk_score = 0
    
    # Factor 1: Communication Link Strength (from our graph)
    # Convert to lowercase to match graph data
    sender = sender.lower()
    recipient = recipient.lower()

    if G.has_node(sender) and G.has_node(recipient):
        if G.has_edge(sender, recipient):
            # They have communicated before. Lower risk.
            weight = G[sender][recipient]['weight']
            evidence_factors.append({
                "finding": "Established Communication Link",
                "details": f"Sender and recipient have exchanged {weight} email(s) before.",
                "risk_contribution": -10 # Negative value reduces risk
            })
        else:
            # They have NOT communicated before. High risk.
            evidence_factors.append({
                "finding": "No Prior Communication",
                "details": "No direct email history found from sender to recipient.",
                "risk_contribution": 40
            })
    else:
        # One or both parties are unknown to the network. Moderate risk.
        evidence_factors.append({
            "finding": "Unknown Entity",
            "details": "Sender and/or recipient not found in the communication network.",
            "risk_contribution": 20
        })

    # Factor 2: Content Analysis for Risky Keywords (using spaCy)
    risky_keywords = {
        "financial": ["invoice", "payment", "bank", "account", "transfer", "wire"],
        "urgency": ["urgent", "asap", "immediate", "now", "action required"],
        "credential": ["password", "username", "login", "verify", "authenticate"]
    }
    
    doc = nlp(body.lower())
    found_keywords = set()

    for token in doc:
        for category, keywords in risky_keywords.items():
            if token.lemma_ in keywords: # Use lemma_ for root form of word
                found_keywords.add(category)
    
    if "financial" in found_keywords:
        evidence_factors.append({
            "finding": "Financial Request Detected",
            "details": "Email contains keywords related to financial transactions.",
            "risk_contribution": 25
        })
    if "urgency" in found_keywords:
        evidence_factors.append({
            "finding": "High Urgency Language Detected",
            "details": "Email contains language creating a sense of urgency.",
            "risk_contribution": 15
        })
    if "credential" in found_keywords:
        evidence_factors.append({
            "finding": "Credential Request Detected",
            "details": "Email contains keywords related to login credentials.",
            "risk_contribution": 30
        })

    # Calculate final risk score
    for factor in evidence_factors:
        risk_score += factor['risk_contribution']
    
    # Clamp the score between 0 and 100
    risk_score = max(0, min(100, risk_score))

    return {"risk_score": risk_score, "evidence_factors": evidence_factors}


@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze an email."""
    data = request.json
    
    # Basic validation
    if not data or 'sender' not in data or 'recipient' not in data or 'body' not in data:
        return jsonify({"error": "Missing required fields: sender, recipient, body"}), 400
        
    sender = data['sender']
    recipient = data['recipient']
    body = data['body']
    
    result = analyze_email(sender, recipient, body)
    
    return jsonify(result)


# --- Main execution ---
if __name__ == '__main__':
    # This will run the app on a local development server
    app.run(debug=True)