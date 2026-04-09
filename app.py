import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SNS Pro Negotiator", page_icon="🤝", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 1px solid #1f77b4; }
    .stButton>button:hover { background-color: #1f77b4; color: white; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "strategy_log" not in st.session_state:
    st.session_state.strategy_log = []
if "tension" not in st.session_state:
    st.session_state.tension = 20  # Starts at 20%
if "current_price" not in st.session_state:
    st.session_state.current_price = 4999
if "game_over" not in st.session_state:
    st.session_state.game_over = False

def add_message(role, text):
    st.session_state.chat_history.append({"role": role, "content": text})

def apply_move(user_text, strategy, price_change, tension_change):
    add_message("user", user_text)
    st.session_state.strategy_log.append(strategy)
    st.session_state.current_price = price_change
    st.session_state.tension += tension_change
    st.session_state.stage += 1
    
    # Cap tension between 0 and 100
    st.session_state.tension = max(0, min(100, st.session_state.tension))
    if st.session_state.tension >= 100:
        st.session_state.game_over = True

def reset_game():
    for key in ["stage", "chat_history", "strategy_log", "game_over"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.tension = 20
    st.session_state.current_price = 4999

# --- HEADER ---
st.title("🤝 Advanced Retail Negotiation Simulator")
st.markdown("Navigate the conversation, manage the salesperson's tension, and find the ZOPA.")
st.divider()

# --- LAYOUT: TWO COLUMNS ---
col_chat, col_stats = st.columns([2, 1])

with col_stats:
    st.markdown("### 📊 Live Deal Stats")
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    st.metric(label="Current Offer (₹)", value=f"₹{st.session_state.current_price}")
    
    # Tension Progress Bar Color Logic
    if st.session_state.tension < 50:
        bar_color = "🟢" 
    elif st.session_state.tension < 80:
        bar_color = "🟠"
    else:
        bar_color = "🔴"
        
    st.markdown(f"**Deal Tension:** {bar_color}")
    st.progress(st.session_state.tension / 100.0)
    if st.session_state.tension >= 80:
        st.caption("⚠️ *Warning: The salesperson is losing patience!*")
    st.markdown("</div>", unsafe_allow_html=True)

with col_chat:
    # --- INITIALIZE CHAT ---
    if st.session_state.stage == 0 and len(st.session_state.chat_history) == 0:
        add_message("assistant", "Welcome to Max! I see you're looking at our premium winter jacket. The MRP is ₹4,999. It's our best seller this week. Shall I take it to the billing counter?")

    # --- DISPLAY CHAT HISTORY ---
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # --- GAME OVER LOGIC (TENSION MAXED) ---
    if st.session_state.game_over:
        st.error("🚨 **Negotiation Breakdown:** The tension hit 100%. The salesperson got offended and walked away. No deal.")
        if st.button("🔄 Try Again"):
            reset_game()
            st.rerun()
            
    # --- NEGOTIATION STAGES ---
    elif not st.session_state.game_over:
        
        # STAGE 0: The Opening
        if st.session_state.stage == 0:
            st.info("🎯 **Your Turn:** The price is anchored at ₹4,999. Choose your opening tactic:")
            
            op1 = st.button("A) [Aggressive Lowball] '₹4,999? That's ridiculous. I'll give you ₹2,000.'")
            op2 = st.button("B) [BATNA / D2C Leverage] 'Nice jacket, but a direct-to-consumer brand online sells this exact material for ₹3,200. Can you match it?'")
            op3 = st.button("C) [Collaborative Info Gathering] 'It's a bit out of my budget. Are there any upcoming sales or card discounts I can use?'")

            if op1: apply_move("That's ridiculous. I'll give you ₹2,000.", "Aggressive Anchoring", 4999, +60); st.rerun()
            if op2: apply_move("A direct-to-consumer brand online sells this exact material for ₹3,200. Can you match it?", "BATNA Leverage", 4999, +20); st.rerun()
            if op3: apply_move("It's a bit out of my budget. Are there any upcoming sales or card discounts I can use?", "Collaborative", 4999, -10); st.rerun()

        # STAGE 1: Salesperson Counter
        elif st.session_state.stage == 1:
            last_strategy = st.session_state.strategy_log[-1]
            
            if last_strategy == "Aggressive Anchoring":
                bot_reply = "Sir, ₹2,000 is insulting. The absolute best I can do is a 5% manager override, bringing it to ₹4,750. That's my final offer."
                new_price = 4750
            elif last_strategy == "BATNA Leverage":
                bot_reply = "I understand the D2C space is competitive, but they don't offer in-store warranty or immediate fitting. I want to keep your business here. Let's do ₹3,999."
                new_price = 3999
            else:
                bot_reply = "Since you asked nicely, if you download our store app right now, I can apply a first-time user discount of 15%, dropping the price to ₹4,250."
                new_price = 4250
            
            if len(st.session_state.chat_history) == 2:
                add_message("assistant", bot_reply)
                st.session_state.current_price = new_price
                st.rerun()

            st.info("🎯 **Your Turn:** The ZOPA is forming. Make your final push.")
            
            if last_strategy == "Aggressive Anchoring":
                op1 = st.button("A) [Walk Away] 'Still too high. I'm leaving.'")
                op2 = st.button("B) [Push harder] '₹4,000 or I walk.'")
                if op1: apply_move("Still too high. I'm leaving.", "Walk Away", new_price, 0); st.rerun()
                if op2: apply_move("₹4,000 or I walk.", "Hard Ultimatum", new_price, +30); st.rerun()
                
            elif last_strategy == "BATNA Leverage":
                op1 = st.button("A) [Split the Difference] 'Meet me in the middle at ₹3,600 and we have a deal.'")
                op2 = st.button("B) [Accept] '₹3,999 is fair given the instant gratification. Wrap it up.'")
                if op1: apply_move("Meet me in the middle at ₹3,600 and we have a deal.", "Compromising", new_price, +10); st.rerun()
                if op2: apply_move("₹3,999 is fair. Wrap it up.", "Acceptance", new_price, 0); st.rerun()
                
            else:
                op1 = st.button("A) [Expand the Pie] 'I'll download the app and pay ₹4,250 if you throw in a pair of socks.'")
                op2 = st.button("B) [Accept] 'Great, let's do the app discount.'")
                if op1: apply_move("I'll do the app, but throw in some socks.", "Value Creation", new_price, +5); st.rerun()
                if op2: apply_move("Great, let's do the app discount.", "Acceptance", new_price, 0); st.rerun()

        # STAGE 2: The Outcome
        elif st.session_state.stage == 2:
            last_strategy = st.session_state.strategy_log[-1]
            success = False
            
            if last_strategy == "Walk Away":
                outcome_msg = "*You walk out of the store.*"
            elif last_strategy == "Hard Ultimatum":
                outcome_msg = "Salesperson: 'I literally cannot do that without losing my job. Have a good day.' *Deal breaks down.*"
            elif last_strategy == "Compromising":
                outcome_msg = "Salesperson: '*Sighs* Okay, ₹3,600. Let's get you to the billing counter quickly.' 🎉"
                success = True
                st.session_state.current_price = 3600
            elif last_strategy == "Value Creation":
                outcome_msg = "Salesperson: 'I can't give them for free, but I'll add the socks for just ₹50. Deal?' 🤝"
                success = True
            else:
                outcome_msg = "Salesperson: 'Excellent choice! Let me pack that up for you right away.' 🎉"
                success = True

            if len(st.session_state.chat_history) == 4:
                add_message("assistant", outcome_msg)
                st.rerun()
            
            st.divider()
            st.subheader("📊 Grading & Analysis")
            if success:
                st.success("Target Reached! You successfully negotiated a deal without breaking the salesperson's patience.")
            else:
                st.error("No Deal. Review your conflict management approach.")
            
            if st.button("🔄 Play Again"):
                reset_game()
                st.rerun()
