import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SNS Pro Negotiator", page_icon="🛍️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 1px solid #1f77b4; }
    .stButton>button:hover { background-color: #1f77b4; color: white; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- PRODUCT CATALOG ---
CATALOG = {
    "Premium Winter Jacket": {"mrp": 4999, "emoji": "🧥", "type": "jacket"},
    "Pro Running Shoes": {"mrp": 3599, "emoji": "👟", "type": "shoes"},
    "Silk Blend Formal Shirt": {"mrp": 1999, "emoji": "👔", "type": "shirt"},
    "Designer Aviators": {"mrp": 2499, "emoji": "🕶️", "type": "sunglasses"}
}

# --- SESSION STATE INITIALIZATION ---
if "phase" not in st.session_state:
    st.session_state.phase = "storefront" 
if "wallet" not in st.session_state:
    st.session_state.wallet = 10000 
if "purchases" not in st.session_state:
    st.session_state.purchases = []
if "failed_deals" not in st.session_state: # Tracks failed negotiations
    st.session_state.failed_deals = []

def init_negotiation_state():
    st.session_state.stage = 0
    st.session_state.chat_history = []
    st.session_state.strategy_log = []
    st.session_state.tension = 20
    st.session_state.current_price = CATALOG[st.session_state.selected_item]["mrp"]
    st.session_state.game_over = False

def add_message(role, text):
    st.session_state.chat_history.append({"role": role, "content": text})

def apply_move(user_text, strategy, price_change, tension_change):
    add_message("user", user_text)
    st.session_state.strategy_log.append(strategy)
    st.session_state.current_price = price_change
    st.session_state.tension += tension_change
    st.session_state.stage += 1
    
    st.session_state.tension = max(0, min(100, st.session_state.tension))
    if st.session_state.tension >= 100:
        st.session_state.game_over = True

def return_to_store():
    st.session_state.phase = "storefront"

# --- HEADER ---
st.title("🛍️ Advanced Retail Simulator")
st.markdown("Manage your budget, choose your targets, and test your negotiation skills.")
st.divider()


# ==========================================
# PHASE 1: THE STOREFRONT
# ==========================================
if st.session_state.phase == "storefront":
    st.subheader("🛒 Max Storefront")
    
    col1, col2 = st.columns([3, 1])
    
    # RIGHT COLUMN: WALLET & RESET
    with col2:
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.metric("💳 Your Wallet", f"₹{st.session_state.wallet}")
        if st.session_state.purchases:
            st.write("**Inventory:**")
            for item in st.session_state.purchases:
                st.write(f"- ✅ {item}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Reset Game Button
        if st.button("🔄 Reset Entire Game", type="primary"):
            st.session_state.wallet = 10000
            st.session_state.purchases = []
            st.session_state.failed_deals = []
            st.rerun()

    # LEFT COLUMN: PRODUCT GRID
    with col1:
        st.write("Select an item to approach the salesperson about:")
        cols = st.columns(4)
        for i, (item_name, details) in enumerate(CATALOG.items()):
            with cols[i % 4]:
                # Using Streamlit's native container for a clean box layout
                with st.container(border=True):
                    
                    # 1. Status Indicator
                    if item_name in st.session_state.purchases:
                        st.markdown("<p style='text-align:center; color: #28a745; font-weight:bold; margin-bottom: 5px;'>✅ Deal Done</p>", unsafe_allow_html=True)
                    elif item_name in st.session_state.failed_deals:
                        st.markdown("<p style='text-align:center; color: #dc3545; font-weight:bold; margin-bottom: 5px;'>❌ No Deal</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='text-align:center; color: gray; margin-bottom: 5px;'>🟢 Available</p>", unsafe_allow_html=True)
                    
                    # 2. Product Details
                    st.markdown(f"<h1 style='text-align:center; margin-top: 0;'>{details['emoji']}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center;'><strong>{item_name}</strong><br>MRP: ₹{details['mrp']}</p>", unsafe_allow_html=True)
                    
                    # 3. Dynamic Button Logic
                    if item_name in st.session_state.purchases:
                        st.button("Purchased", key=item_name, disabled=True)
                    elif st.session_state.wallet < details['mrp'] * 0.5:
                        st.button("Insufficient Funds", key=item_name, disabled=True)
                    else:
                        btn_text = "Retry Negotiation" if item_name in st.session_state.failed_deals else "Negotiate"
                        if st.button(btn_text, key=item_name):
                            st.session_state.selected_item = item_name
                            st.session_state.phase = "negotiation"
                            init_negotiation_state()
                            st.rerun()


# ==========================================
# PHASE 2: THE NEGOTIATION
# ==========================================
elif st.session_state.phase == "negotiation":
    item = st.session_state.selected_item
    mrp = CATALOG[item]["mrp"]
    item_type = CATALOG[item]["type"]
    
    col_chat, col_stats = st.columns([2, 1])

    with col_stats:
        st.markdown("### 📊 Live Deal Stats")
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.metric(label="Target Item", value=f"{CATALOG[item]['emoji']} {item}")
        st.metric(label="Current Offer (₹)", value=f"₹{int(st.session_state.current_price)}")
        st.metric(label="💳 Wallet Balance", value=f"₹{st.session_state.wallet}")
        
        if st.session_state.tension < 50: bar_color = "🟢" 
        elif st.session_state.tension < 80: bar_color = "🟠"
        else: bar_color = "🔴"
            
        st.markdown(f"**Deal Tension:** {bar_color}")
        st.progress(st.session_state.tension / 100.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚪 Leave Conversation"):
            return_to_store()
            st.rerun()

    with col_chat:
        lowball_price = int(mrp * 0.4)
        batna_price = int(mrp * 0.65)
        manager_price = int(mrp * 0.95)
        match_price = int(mrp * 0.8)
        app_price = int(mrp * 0.85)
        split_price = int((match_price + batna_price) / 2)

        if st.session_state.stage == 0 and len(st.session_state.chat_history) == 0:
            add_message("assistant", f"Welcome! I see you're looking at our {item_type}. The MRP is ₹{mrp}. It's a great choice. Shall I bill it for you?")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if st.session_state.game_over:
            st.error("🚨 **Negotiation Breakdown:** The tension hit 100%. The salesperson got offended and walked away. No deal.")
            # Record the failure
            if item not in st.session_state.failed_deals:
                st.session_state.failed_deals.append(item)
            if st.button("Return to Store"):
                return_to_store()
                st.rerun()
                
        elif not st.session_state.game_over:
            
            # STAGE 0
            if st.session_state.stage == 0:
                st.info(f"🎯 **Your Turn:** The price is anchored at ₹{mrp}.")
                
                op1 = st.button(f"A) [Aggressive Lowball] '₹{mrp}? That's ridiculous. I'll give you ₹{lowball_price}.'")
                op2 = st.button(f"B) [BATNA / D2C Leverage] 'Nice {item_type}, but a D2C brand online sells this for ₹{batna_price}. Can you match it?'")
                op3 = st.button(f"C) [Collaborative Info Gathering] 'It's a bit out of my budget. Are there any store discounts I can use?'")

                if op1: apply_move(f"That's ridiculous. I'll give you ₹{lowball_price}.", "Aggressive Anchoring", mrp, +60); st.rerun()
                if op2: apply_move(f"A brand online sells this for ₹{batna_price}. Can you match it?", "BATNA Leverage", mrp, +20); st.rerun()
                if op3: apply_move("Are there any ongoing sales or discounts?", "Collaborative", mrp, -10); st.rerun()

            # STAGE 1
            elif st.session_state.stage == 1:
                last_strategy = st.session_state.strategy_log[-1]
                
                if last_strategy == "Aggressive Anchoring":
                    bot_reply = f"Sir, ₹{lowball_price} is insulting. The absolute best I can do is a 5% manager override, bringing it to ₹{manager_price}. That's my final offer."
                    new_price = manager_price
                elif last_strategy == "BATNA Leverage":
                    bot_reply = f"I understand the D2C space is competitive, but they don't offer in-store warranty. Let's do ₹{match_price}."
                    new_price = match_price
                else:
                    bot_reply = f"Since you asked nicely, if you download our store app right now, I can apply a discount, dropping the price to ₹{app_price}."
                    new_price = app_price
                
                if len(st.session_state.chat_history) == 2:
                    add_message("assistant", bot_reply)
                    st.session_state.current_price = new_price
                    st.rerun()

                st.info("🎯 **Your Turn:** The ZOPA is forming. Make your final push.")
                
                if last_strategy == "Aggressive Anchoring":
                    op1 = st.button("A) [Walk Away] 'Still too high. I'm leaving.'")
                    op2 = st.button(f"B) [Push harder] '₹{int(mrp * 0.8)} or I walk.'")
                    if op1: apply_move("Still too high. I'm leaving.", "Walk Away", new_price, 0); st.rerun()
                    if op2: apply_move(f"₹{int(mrp * 0.8)} or I walk.", "Hard Ultimatum", new_price, +30); st.rerun()
                    
                elif last_strategy == "BATNA Leverage":
                    op1 = st.button(f"A) [Split the Difference] 'Meet me in the middle at ₹{split_price} and we have a deal.'")
                    op2 = st.button(f"B) [Accept] '₹{match_price} is fair. Wrap it up.'")
                    if op1: apply_move(f"Meet me in the middle at ₹{split_price} and we have a deal.", "Compromising", new_price, +10); st.rerun()
                    if op2: apply_move(f"₹{match_price} is fair. Wrap it up.", "Acceptance", new_price, 0); st.rerun()
                    
                else:
                    op1 = st.button(f"A) [Expand the Pie] 'I'll pay ₹{app_price} if you throw in a free cleaning kit.'")
                    op2 = st.button("B) [Accept] 'Great, let's do the app discount.'")
                    if op1: apply_move("I'll do the app, but throw in a cleaning kit.", "Value Creation", new_price, +5); st.rerun()
                    if op2: apply_move("Great, let's do the app discount.", "Acceptance", new_price, 0); st.rerun()

            # STAGE 2
            elif st.session_state.stage == 2:
                last_strategy = st.session_state.strategy_log[-1]
                success = False
                final_paid = st.session_state.current_price
                
                if last_strategy == "Walk Away":
                    outcome_msg = "*You walk away from the counter.*"
                elif last_strategy == "Hard Ultimatum":
                    outcome_msg = "Salesperson: 'I literally cannot do that without losing my job. Have a good day.' *Deal breaks down.*"
                elif last_strategy == "Compromising":
                    outcome_msg = f"Salesperson: '*Sighs* Okay, ₹{split_price}. Let's get you to the billing counter quickly.' 🎉"
                    success = True
                    final_paid = split_price
                elif last_strategy == "Value Creation":
                    outcome_msg = "Salesperson: 'I can't give it for free, but I'll add the kit for just ₹50. Deal?' 🤝"
                    success = True
                else:
                    outcome_msg = "Salesperson: 'Excellent choice! Let me pack that up for you right away.' 🎉"
                    success = True

                if len(st.session_state.chat_history) == 4:
                    add_message("assistant", outcome_msg)
                    st.session_state.current_price = final_paid 
                    
                    if success:
                        st.session_state.wallet -= final_paid
                        st.session_state.purchases.append(item)
                        if item in st.session_state.failed_deals:
                            st.session_state.failed_deals.remove(item) # Remove failure badge if they retry and succeed
                    else:
                        if item not in st.session_state.failed_deals:
                            st.session_state.failed_deals.append(item) # Add failure badge
                    
                    st.rerun()
                
                st.divider()
                if success:
                    st.success(f"Deal Closed! You paid ₹{final_paid} for the {item}. The amount has been deducted from your wallet.")
                else:
                    st.error("No Deal. You kept your money but left without the item.")
                
                if st.button("🛒 Return to Storefront"):
                    return_to_store()
                    st.rerun()
