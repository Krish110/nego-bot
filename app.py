import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SNS Negotiation Simulator", page_icon="🛍️", layout="centered")

# --- CUSTOM CSS FOR UI ---
st.markdown("""
<style>
    .stRadio > label { font-weight: bold; color: #1f77b4; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    .success-text { color: #28a745; font-size: 18px; font-weight: bold;}
    .fail-text { color: #dc3545; font-size: 18px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "strategy_log" not in st.session_state:
    st.session_state.strategy_log = []

def add_message(role, text):
    st.session_state.chat_history.append({"role": role, "content": text})

def next_stage(user_choice_text, concept_used):
    add_message("user", user_choice_text)
    st.session_state.strategy_log.append(concept_used)
    st.session_state.stage += 1
    
def reset_game():
    st.session_state.stage = 0
    st.session_state.chat_history = []
    st.session_state.strategy_log = []

# --- APP HEADER ---
st.title("🛍️ Max Retail Negotiation Bot")
st.markdown("**Role:** Buyer | **Opponent:** Max Store Manager")
st.markdown("*Test your Sales & Negotiation Skills (SNS). Choose your strategy wisely!*")
st.divider()

# --- INITIALIZE CHAT ---
if st.session_state.stage == 0 and len(st.session_state.chat_history) == 0:
    add_message("assistant", "Welcome to Max! I see you're looking at our premium winter jacket collection. The MRP is ₹4,999. Since it's new stock, it's selling fast. Can I bill this for you?")

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- NEGOTIATION LOGIC & TRAJECTORIES ---

# STAGE 0: The Opening Counter
if st.session_state.stage == 0:
    st.info("🎯 **Your Turn:** The salesperson has anchored the price at ₹4,999. How do you respond?")
    
    choice = st.radio("Choose your negotiation strategy:", [
        "A) [Aggressive / Lowball] 'That's way too high. I'll give you ₹2,500 for it right now.'",
        "B) [BATNA Approach] 'I really like it, but I saw a very similar jacket online on Myntra for ₹3,500. Can you match that?'",
        "C) [Collaborative] 'It's a great jacket, but slightly out of my budget. Is there any ongoing store discount we can apply?'"
    ], index=None)
    
    if st.button("Send Response", disabled=(choice is None)):
        if choice.startswith("A"):
            next_stage(choice, "Aggressive Lowball (Risky)")
        elif choice.startswith("B"):
            next_stage(choice, "Leveraging BATNA")
        else:
            next_stage(choice, "Collaborative Problem Solving")
        st.rerun()

# STAGE 1: The Salesperson's Reaction
elif st.session_state.stage == 1:
    last_strategy = st.session_state.strategy_log[-1]
    
    # Generate bot response based on user's previous choice
    if last_strategy == "Aggressive Lowball (Risky)":
        bot_reply = "Sir, ₹2,500 is far below our cost price. The maximum I can do is a 5% manager discount, bringing it to ₹4,750. Take it or leave it."
    elif last_strategy == "Leveraging BATNA":
        bot_reply = "I understand, but online stores don't let you check the fabric quality like we do here. Plus, no wait for delivery! I want to close this deal. Let's meet halfway at ₹3,999."
    else:
        bot_reply = "I appreciate your honesty! We don't have a flat discount on this item, but if you sign up for our loyalty program today, I can give you a 15% discount, bringing it down to ₹4,250."
    
    if len(st.session_state.chat_history) == 2: # Ensure we only add it once
        add_message("assistant", bot_reply)
        st.rerun()

    st.info("🎯 **Your Turn:** The ZOPA (Zone of Possible Agreement) is becoming clearer. Make your final move.")
    
    if last_strategy == "Aggressive Lowball (Risky)":
        final_choice = st.radio("Choose your final action:", [
            "A) [Walk Away] 'Still too high. I'm leaving.'",
            "B) [Concede] 'Fine, pack it for ₹4,750.'"
        ], index=None)
    elif last_strategy == "Leveraging BATNA":
        final_choice = st.radio("Choose your final action:", [
            "A) [Push for Reservation Price] 'Make it ₹3,700 and I'll buy it right now without looking anywhere else.'",
            "B) [Accept] '₹3,999 sounds fair. Let's do it.'"
        ], index=None)
    else:
        final_choice = st.radio("Choose your final action:", [
            "A) [Value Addition] 'I'll take it for ₹4,250 if you throw in a pair of those ₹300 socks for free.'",
            "B) [Accept] 'Okay, sign me up for the loyalty program. I'll take it.'"
        ], index=None)

    if st.button("Finalize Deal", disabled=(final_choice is None)):
        if final_choice.startswith("A"):
             next_stage(final_choice, "Hard Push / Bundle")
        else:
             next_stage(final_choice, "Acceptance / Concession")
        st.rerun()

# STAGE 2: The Outcome & Analysis
elif st.session_state.stage == 2:
    last_strategy = st.session_state.strategy_log[-2]
    final_action = st.session_state.strategy_log[-1]
    
    # Calculate Final Outcome
    if last_strategy == "Aggressive Lowball (Risky)" and final_action == "Hard Push / Bundle":
        outcome_msg = "Salesperson: 'I'm sorry sir, I cannot go any lower. Have a good day.' \n\n*The salesperson packs up the jacket. Negotiation failed.*"
        success = False
    elif last_strategy == "Leveraging BATNA" and final_action == "Hard Push / Bundle":
        outcome_msg = "Salesperson: '*Sighs* Alright, ₹3,700 it is. But please don't tell the other customers! Let's get you billed.'"
        success = True
    elif last_strategy == "Collaborative Problem Solving" and final_action == "Hard Push / Bundle":
        outcome_msg = "Salesperson: 'You drive a hard bargain! I can't give the socks for free, but I can give them to you at 50% off along with the jacket for ₹4,250. Deal?' \n\n*You shake hands. Deal closed!*"
        success = True
    else:
        outcome_msg = "Salesperson: 'Excellent choice! Let me pack that up for you right away.'"
        success = True

    if len(st.session_state.chat_history) == 4:
        add_message("assistant", outcome_msg)
        st.rerun()

    st.divider()
    if success:
        st.markdown("<p class='success-text'>🎉 Deal Successfully Closed!</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='fail-text'>❌ Negotiation Broke Down. No Deal.</p>", unsafe_allow_html=True)

    # --- ACADEMIC DEBRIEF ---
    st.subheader("📊 SNS Concepts Debrief")
    st.write("**Your Selected Trajectory:**")
    for i, step in enumerate(st.session_state.strategy_log):
        st.write(f"{i+1}. {step}")
    
    st.write("**Analysis of this run:**")
    if last_strategy == "Leveraging BATNA":
        st.write("By establishing a strong **BATNA** (the Myntra online price), you effectively shifted the anchoring power away from the salesperson. This forced them to justify their premium and immediately drop their price to find the **ZOPA**.")
    elif last_strategy == "Aggressive Lowball (Risky)":
        st.write("Your extreme initial counter-offer created a hostile **Conflict Management** scenario. While aggressive anchoring can work, doing it without justification often causes the other party to lock into a defensive reservation price, risking a deal breakdown.")
    elif last_strategy == "Collaborative Problem Solving":
        st.write("You adopted an **Accommodating/Collaborative** style. Instead of fighting over the core price, you allowed the salesperson to find creative solutions (loyalty programs, bundling). This is a great way to expand the pie when the ZOPA is tight.")

    if st.button("🔄 Restart Simulation"):
        reset_game()
        st.rerun()  
