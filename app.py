import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SNS Negotiation Challenge", page_icon="🛍️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; border: 1px solid #1f77b4; }
    .stButton>button:hover { background-color: #1f77b4; color: white; }
    .status-box { padding: 15px; border-radius: 10px; background-color: rgba(128, 128, 128, 0.1); margin-bottom: 20px;}
    .debrief-box { padding: 20px; border-left: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1); margin-top: 20px; border-radius: 5px;}
    .debrief-box-success { border-left: 5px solid #28a745; background-color: rgba(40, 167, 69, 0.1); }
</style>
""", unsafe_allow_html=True)

# --- PRODUCT CATALOG, UNIQUE SCENARIOS & ACADEMIC DEBRIEFS ---
SCENARIOS = {
    "Premium Winter Jacket": {
        "mrp": 4999, "emoji": "🧥", "type": "jacket",
        "intro": "Welcome! Looking at the premium winter jacket? It's our best seller. The MRP is ₹4999.",
        "stage0": [
            {"text": "A) [Hostile Lowball] '₹2000 cash right now. Take it or leave it.'", "strategy": "Hostile Anchoring", "reply": "Sir, ₹2000 is impossible. I would get fired. The absolute best I can do without a manager is ₹4800.", "price": 4800, "tension": 60},
            {"text": "B) [BATNA] 'Myntra has a very similar fleece for ₹3200. Can you match it?'", "strategy": "BATNA Leverage", "reply": "Online quality is different, but I don't want you to leave empty-handed. I can drop it to ₹3999.", "price": 3999, "tension": 15},
            {"text": "C) [Collaborative] 'It's nice, but out of budget. Any card offers?'", "strategy": "Collaborative Value Creation", "reply": "We have an HDFC card offer that brings it down to ₹4500.", "price": 4500, "tension": -5}
        ],
        "stage1": {
            "Hostile Anchoring": [
                {"text": "A) [Walk Away] 'Then I'm leaving.'", "outcome": "fail", "msg": "Salesperson: 'Go ahead. Have a nice day.'", "debrief": "Your extreme initial anchor created a **Competitive** conflict style. Because you anchored far outside the **ZOPA** (Zone of Possible Agreement), the salesperson locked into a defensive **Reservation Price**, resulting in a breakdown."},
                {"text": "B) [Cave In & Pay] 'Fine, bill it at ₹4800.'", "outcome": "success", "price": 4800, "msg": "Salesperson: 'Smart choice. It's a great jacket.'", "debrief": "You started with a Competitive anchor but quickly shifted to an **Accommodating** conflict style. You conceded almost entirely to their counter-offer, resulting in a poor deal for your wallet."}
            ],
            "BATNA Leverage": [
                {"text": "A) [Split Difference] 'Meet me at ₹3500 and I'll buy it right now.'", "outcome": "success", "price": 3500, "msg": "Salesperson: '*Sigh* Alright, ₹3500. Just don't tell my manager.'", "debrief": "Excellent execution. You established a strong **BATNA** (Myntra) to shift the power dynamic, then used a **Compromising** style to find a mutual **ZOPA**, successfully pulling the final price toward your target."},
                {"text": "B) [Push Harder] 'Match ₹3200 or I order it online.'", "outcome": "fail", "msg": "Salesperson: 'I really can't go that low. You'll have to order it online.'", "debrief": "You leveraged your **BATNA**, but you pushed past the salesperson's absolute **Reservation Price**. Sometimes, a retail store's overhead means their ZOPA simply cannot match an online competitor."}
            ],
            "Collaborative Value Creation": [
                {"text": "A) [Value Add] 'I'll take it for ₹4500 if you add a ₹500 t-shirt for free.'", "outcome": "success", "price": 4500, "msg": "Salesperson: 'I can't make it free, but I'll give the t-shirt at 80% off. Let's bill it.'", "debrief": "Textbook **Collaborative** negotiation! Instead of fighting over a single variable (price), you attempted to 'expand the pie' by bundling. This builds rapport and secures extra value."},
                {"text": "B) [Accept] 'Okay, ₹4500 works.'", "outcome": "success", "price": 4500, "msg": "Salesperson: 'Great, let's head to the counter.'", "debrief": "You used a polite, **Accommodating** approach. While you secured a discount without creating tension, you likely left money on the table by accepting their first counter-offer without pushing further into the **ZOPA**."}
            ]
        }
    },
    "Pro Running Shoes": {
        "mrp": 3599, "emoji": "👟", "type": "shoes",
        "intro": "These have the new responsive foam technology. MRP is ₹3599.",
        "stage0": [
            {"text": "A) [Tech Expertise] 'The foam is outdated compared to Nike's EVA. I'll give you ₹2500.'", "strategy": "Objective Criteria", "reply": "You know your shoes! Okay, they aren't Nikes, but they are durable. I can do ₹2800.", "price": 2800, "tension": 10},
            {"text": "B) [Indifference] 'They look okay. I might just stick to my old ones.'", "strategy": "Avoiding Style", "reply": "Wait, don't leave! If you buy them today, I can apply a staff discount. ₹3000.", "price": 3000, "tension": 0},
            {"text": "C) [Aggressive] 'Nobody buys this brand. ₹1500.'", "strategy": "Hostile Anchoring", "reply": "Excuse me? This is a highly rated shoe. The lowest I'll go is ₹3400.", "price": 3400, "tension": 50}
        ],
        "stage1": {
            "Objective Criteria": [
                {"text": "A) [Final Push] 'Make it ₹2600 and I'll wear them out of the store.'", "outcome": "success", "price": 2600, "msg": "Salesperson: 'You drive a hard bargain. ₹2600 it is.'", "debrief": "By using **Objective Criteria** (technical specs) rather than emotion, you logically devalued their product. This gave you the leverage to dictate a favorable **ZOPA**."},
                {"text": "B) [Walk] 'Still too much for old tech.'", "outcome": "fail", "msg": "Salesperson: 'Suit yourself.'", "debrief": "You used objective facts well, but your rigid target price was below their **Reservation Price**. A slight compromise was needed to close."}
            ],
            "Avoiding Style": [
                {"text": "A) [Sunk Cost] 'Eh, ₹3000 is still high. ₹2800?'", "outcome": "success", "price": 2800, "msg": "Salesperson: 'Okay, ₹2800. Let's get it packed.'", "debrief": "Feigning an **Avoiding** conflict style (indifference) forces the other party to chase you. Once they opened the **ZOPA**, you effectively counter-anchored."},
                {"text": "B) [Accept] 'Alright, ₹3000 is fair.'", "outcome": "success", "price": 3000, "msg": "Salesperson: 'Excellent choice.'", "debrief": "The avoiding strategy worked to trigger a discount, but you acted as an **Accommodator** by immediately taking the first concession."}
            ],
            "Hostile Anchoring": [
                {"text": "A) [Apologize & Pay] 'Sorry, ₹3400 is fine.'", "outcome": "success", "price": 3400, "msg": "Salesperson: 'Right. Follow me to the counter.'", "debrief": "You attempted an aggressive anchor, met resistance, and immediately folded. This is a classic **Competitive -> Accommodating** fail state, yielding terrible financial results."},
                {"text": "B) [Double Down] '₹1500 or nothing.'", "outcome": "fail", "msg": "Salesperson: 'Then it's nothing. Goodbye.'", "debrief": "A purely **Competitive** approach with no justification. You never found the **ZOPA** because you refused to acknowledge the salesperson's baseline needs."}
            ]
        }
    },
    "Designer Aviators": {
        "mrp": 2499, "emoji": "🕶️", "type": "sunglasses",
        "intro": "Good eye on the Aviators. That's actually the last piece we have in stock! MRP is ₹2499.",
        "stage0": [
            {"text": "A) [Call Bluff] 'It's a display piece, there are smudges. I'll take it for ₹1200.'", "strategy": "Devaluation", "reply": "Oh, I can clean the smudges! Look, since it is the display model, I can do ₹1800.", "price": 1800, "tension": 30},
            {"text": "B) [FOMO Victim] 'Last piece? Oh man. Is there any discount at all?'", "strategy": "Information Yielding", "reply": "Since it's the last one, I usually don't discount. But I'll knock off ₹100. ₹2399.", "price": 2399, "tension": 0},
            {"text": "C) [Bundle] 'I'll pay ₹2499 if you throw in a premium hard case.'", "strategy": "Value Creation", "reply": "I can't give the premium case, but I'll give you the standard hard case for free at ₹2499.", "price": 2499, "tension": 0}
        ],
        "stage1": {
            "Devaluation": [
                {"text": "A) [Firm Hold] '₹1500 is my final offer for a scratched display piece.'", "outcome": "success", "price": 1500, "msg": "Salesperson: 'Fine, ₹1500. I just want to clear the inventory.'", "debrief": "You brilliantly neutralized their 'Scarcity' tactic by pointing out flaws (**Devaluation**). You held firm to your **Target Price**, forcing them to yield."},
                {"text": "B) [Accept] '₹1800 works.'", "outcome": "success", "price": 1800, "msg": "Salesperson: 'Great, I'll wipe them down for you.'", "debrief": "Good use of devaluation to drop the anchor. Accepting ₹1800 shows a **Compromising** style, ensuring the deal closes smoothly."}
            ],
            "Information Yielding": [
                {"text": "A) [Beg] 'Please, any lower? My budget is tight.'", "outcome": "fail", "msg": "Salesperson: 'Sorry, I have another customer coming to look at these later anyway.'", "debrief": "By showing desperation (FOMO), you yielded all your **Negotiation Power**. The salesperson felt no need to adjust their **Reservation Price**."},
                {"text": "B) [Pay up] 'Okay, ₹2399.'", "outcome": "success", "price": 2399, "msg": "Salesperson: 'You won't regret securing the last one!'", "debrief": "You fell victim to the psychological trigger of 'Scarcity'. You ignored your **BATNA** and accepted a price barely inside the top edge of the **ZOPA**."}
            ],
            "Value Creation": [
                {"text": "A) [Greedy Push] 'Actually, make it ₹2000 AND the case.'", "outcome": "fail", "msg": "Salesperson: 'Now you're just being unreasonable. The deal is off.'", "debrief": "You successfully collaborated to expand the pie, but then greedily shifted to a **Competitive** style. This erratic behavior shattered trust and broke the deal."},
                {"text": "B) [Accept] 'Deal. Wrap the case and glasses.'", "outcome": "success", "price": 2499, "msg": "Salesperson: 'Perfect, let's head to billing.'", "debrief": "You paid full price but gained extra utility. This is classic **Integrative Bargaining**—finding a win-win without technically altering the primary cash **ZOPA**."}
            ]
        }
    },
    "Silk Formal Shirt": {
        "mrp": 1999, "emoji": "👔", "type": "shirt",
        "intro": "Ah, the Silk Blend Formal. Perfect for corporate wear. MRP is ₹1999.",
        "stage0": [
            {"text": "A) [Nitpicking] 'There's a loose thread on the cuff. I'll give you ₹1000.'", "strategy": "Devaluation", "reply": "Sir, that's just a surface fiber, the stitching is intact. The lowest I can go is ₹1800.", "price": 1800, "tension": 40},
            {"text": "B) [Student/Corp ID] 'Do you offer a student or corporate discount on formal wear?'", "strategy": "Policy Leverage", "reply": "Yes, with a valid college or corporate ID, I can apply a flat discount, bringing it to ₹1699.", "price": 1699, "tension": -5},
            {"text": "C) [Volume Bluff] 'If I was buying 5 of these, what would the price be? Apply that to just this one.'", "strategy": "Hypothetical Anchoring", "reply": "Haha, I appreciate the hustle, but volume discounts require actual volume. I'll meet you at ₹1750.", "price": 1750, "tension": 10}
        ],
        "stage1": {
            "Devaluation": [
                {"text": "A) [Hold Ground] '₹1400 or I buy it from Zara.'", "outcome": "success", "price": 1400, "msg": "Salesperson: 'Fine, ₹1400. But no returns on discounted items.'", "debrief": "By combining a product flaw with a strong **BATNA** (Zara), you completely overpowered the salesperson's initial anchor, forcing them to their bottom **Reservation Price**."},
                {"text": "B) [Walk Away] 'Never mind, I don't want damaged goods.'", "outcome": "fail", "msg": "Salesperson: 'It's not damaged, but okay. Have a good day.'", "debrief": "You successfully devalued the item, but by walking away you exercised an **Avoiding** style, missing a clear opportunity to establish a **ZOPA**."}
            ],
            "Policy Leverage": [
                {"text": "A) [Push for Round Number] 'Make it an even ₹1500 and we have a deal.'", "outcome": "success", "price": 1500, "msg": "Salesperson: 'Alright, ₹1500. I'll process it under our special promo code.'", "debrief": "You used objective **Policy Leverage** to drop the price instantly, then applied a subtle psychological push ('round numbers') to squeeze out final value."},
                {"text": "B) [Accept] '₹1699 sounds fair.'", "outcome": "success", "price": 1699, "msg": "Salesperson: 'Great, please keep your ID handy for billing.'", "debrief": "A clean, frictionless transaction. While you saved money using policy, accepting the first counter-offer means you likely left the bottom 10% of the **ZOPA** untapped."}
            ],
            "Hypothetical Anchoring": [
                {"text": "A) [Push Harder] 'Come on, just do ₹1600.'", "outcome": "fail", "msg": "Salesperson: 'I can't authorize that. ₹1750 is my limit. Since we can't agree, let's just leave it.'", "debrief": "Your 'volume bluff' was seen through. Pushing harder on a failed bluff broke rapport. The salesperson preferred to walk away than reward a **Competitive** bluff."},
                {"text": "B) [Accept] 'Fair enough, ₹1750 it is.'", "outcome": "success", "price": 1750, "msg": "Salesperson: 'Smart choice. It's a great shirt.'", "debrief": "Your 'volume bluff' failed to secure massive discounts, but you gracefully shifted to an **Accommodating** style to salvage the deal within the upper **ZOPA**."}
            ]
        }
    }
}

# --- SESSION STATE INITIALIZATION ---
if "phase" not in st.session_state: st.session_state.phase = "storefront" 
if "wallet" not in st.session_state: st.session_state.wallet = 7500 
if "purchases" not in st.session_state: st.session_state.purchases = []
if "failed_deals" not in st.session_state: st.session_state.failed_deals = []
if "current_debrief" not in st.session_state: st.session_state.current_debrief = ""

def init_negotiation(item_name):
    st.session_state.selected_item = item_name
    st.session_state.stage = 0
    st.session_state.chat_history = [{"role": "assistant", "content": SCENARIOS[item_name]["intro"]}]
    st.session_state.strategy_log = []
    st.session_state.tension = 20
    st.session_state.current_price = SCENARIOS[item_name]["mrp"]
    st.session_state.game_over = False
    st.session_state.current_debrief = ""
    st.session_state.phase = "negotiation"

# --- HEADER ---
st.title("🛍️ The ₹7.5k Challenge: Retail Simulator")
st.markdown("**Rule:** You only have **₹7,500**. The total value of the store is over ₹13,000. If you accept bad deals, your wallet will drain and you will fail to buy everything!")
st.divider()

# ==========================================
# PHASE 1: THE STOREFRONT
# ==========================================
if st.session_state.phase == "storefront":
    st.subheader("🛒 Max Storefront")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.metric("💳 Your Wallet", f"₹{st.session_state.wallet}")
        
        if st.session_state.purchases:
            st.write("**Inventory:**")
            for item in st.session_state.purchases:
                st.write(f"- ✅ {item}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🔄 Reset Entire Game", type="primary"):
            st.session_state.wallet = 7500
            st.session_state.purchases = []
            st.session_state.failed_deals = []
            st.rerun()

    with col1:
        cols = st.columns(4)
        for i, (item_name, details) in enumerate(SCENARIOS.items()):
            with cols[i % 4]:
                with st.container(border=True):
                    if item_name in st.session_state.purchases:
                        st.markdown("<p style='text-align:center; color: #28a745; font-weight:bold;'>✅ Deal Done</p>", unsafe_allow_html=True)
                    elif item_name in st.session_state.failed_deals:
                        st.markdown("<p style='text-align:center; color: #dc3545; font-weight:bold;'>❌ Walked Away</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='text-align:center; color: gray;'>🟢 Available</p>", unsafe_allow_html=True)
                    
                    st.markdown(f"<h1 style='text-align:center; margin-top: 0;'>{details['emoji']}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center;'><strong>{item_name}</strong><br>MRP: ₹{details['mrp']}</p>", unsafe_allow_html=True)
                    
                    if item_name in st.session_state.purchases:
                        st.button("Purchased", key=item_name, disabled=True)
                    else:
                        btn_text = "Retry Negotiation" if item_name in st.session_state.failed_deals else "Negotiate"
                        if st.button(btn_text, key=item_name):
                            init_negotiation(item_name)
                            st.rerun()

# ==========================================
# PHASE 2: THE NEGOTIATION
# ==========================================
elif st.session_state.phase == "negotiation":
    item = st.session_state.selected_item
    scenario = SCENARIOS[item]
    
    col_chat, col_stats = st.columns([2, 1])

    with col_stats:
        st.markdown("<div class='status-box'>", unsafe_allow_html=True)
        st.metric(label="Target Item", value=f"{scenario['emoji']} {item}")
        st.metric(label="Current Offer (₹)", value=f"₹{st.session_state.current_price}")
        st.metric(label="💳 Wallet Balance", value=f"₹{st.session_state.wallet}")
        
        if st.session_state.tension < 50: bar_color = "🟢" 
        elif st.session_state.tension < 80: bar_color = "🟠"
        else: bar_color = "🔴"
            
        st.markdown(f"**Deal Tension:** {bar_color}")
        st.progress(st.session_state.tension / 100.0)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if not st.session_state.game_over and st.button("🚪 Walk Away"):
            if item not in st.session_state.failed_deals:
                st.session_state.failed_deals.append(item)
            st.session_state.phase = "storefront"
            st.rerun()

    with col_chat:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if st.session_state.game_over:
            
            # THE ACADEMIC DEBRIEF UI
            st.divider()
            success_status = item in st.session_state.purchases
            box_class = "debrief-box debrief-box-success" if success_status else "debrief-box"
            
            st.markdown(f"""
            <div class='{box_class}'>
                <h3 style='margin-top:0;'>📚 Academic Debrief & Strategy Analysis</h3>
                <p><strong>Your Opening Strategy:</strong> {st.session_state.strategy_log[0] if len(st.session_state.strategy_log) > 0 else 'None'}</p>
                <p><strong>Analysis:</strong> {st.session_state.current_debrief}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("") # Spacer
            if st.button("🛒 Return to Storefront"):
                st.session_state.phase = "storefront"
                st.rerun()
                
        elif st.session_state.stage == 0:
            st.info("🎯 **Choose your opening strategy:**")
            for opt in scenario["stage0"]:
                if st.button(opt["text"]):
                    st.session_state.chat_history.append({"role": "user", "content": opt["text"]})
                    st.session_state.chat_history.append({"role": "assistant", "content": opt["reply"]})
                    st.session_state.strategy_log.append(opt["strategy"])
                    st.session_state.current_price = opt["price"]
                    st.session_state.tension += opt["tension"]
                    st.session_state.stage = 1
                    
                    if st.session_state.tension >= 100:
                        st.session_state.chat_history.append({"role": "assistant", "content": "*The salesperson gets deeply offended and walks away. Deal failed.*"})
                        st.session_state.current_debrief = "You maxed out the tension meter by using a purely hostile approach. This reflects a failure in **Conflict Management**. By ignoring the relational aspect of the negotiation, you destroyed any chance of finding a **ZOPA**."
                        st.session_state.game_over = True
                        if item not in st.session_state.failed_deals: st.session_state.failed_deals.append(item)
                    st.rerun()

        elif st.session_state.stage == 1:
            last_strategy = st.session_state.strategy_log[0]
            st.info("🎯 **The ZOPA is forming. Make your final push:**")
            
            for opt in scenario["stage1"][last_strategy]:
                if st.button(opt["text"]):
                    st.session_state.chat_history.append({"role": "user", "content": opt["text"]})
                    st.session_state.current_debrief = opt["debrief"] # Capture the specific debrief
                    
                    if opt["outcome"] == "fail":
                        st.session_state.chat_history.append({"role": "assistant", "content": opt["msg"]})
                        st.error("❌ Negotiation broke down. You walk away empty-handed.")
                        if item not in st.session_state.failed_deals: st.session_state.failed_deals.append(item)
                        
                    elif opt["outcome"] == "success":
                        final_price = opt["price"]
                        st.session_state.current_price = final_price
                        st.session_state.chat_history.append({"role": "assistant", "content": opt["msg"]})
                        
                        if st.session_state.wallet >= final_price:
                            st.session_state.wallet -= final_price
                            st.session_state.purchases.append(item)
                            if item in st.session_state.failed_deals: st.session_state.failed_deals.remove(item)
                            st.success(f"🎉 Deal Closed! ₹{final_price} deducted from wallet.")
                        else:
                            st.error(f"💳 **CARD DECLINED!** You agreed to pay ₹{final_price}, but you only have ₹{st.session_state.wallet} left. The salesperson laughs as you walk away embarrassed.")
                            if item not in st.session_state.failed_deals: st.session_state.failed_deals.append(item)
                            st.session_state.current_debrief = "You successfully negotiated a **ZOPA**, but failed to monitor your own resources (Budget). In real-world procurement, committing to a contract you cannot fund is a critical failure."
                            
                    st.session_state.game_over = True
                    st.rerun()
