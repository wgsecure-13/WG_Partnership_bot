BOT_TOKEN = 8990571916:AAEHBZdlY6mxVq5u3jgR4n8FOFrc8ZriNN0
ADMIN_CHAT_ID = 208259651
VIP_CHANNEL_LINK = https://t.me/+1L4hHIhGu0E5ZDY9

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ================= CONFIGURATION =================
# Step 1, 2, aur 3 ki details yahan replace karein:
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"          # @BotFather se mila token
ADMIN_CHAT_ID = 123456789                  # @userinfobot wala aapka numeric ID (bina quotes ke)
VIP_CHANNEL_LINK = "https://t.me/+YOUR_VIP_LINK"  # Aapke VIP Channel ka private invite link

# Verification Form ke States
(
    FORM_BROKER,
    FORM_NAME,
    FORM_COUNTRY,
    FORM_EMAIL,
    FORM_ACC_NUM,
    FORM_DEPOSIT,
    FORM_SCREENSHOT,
) = range(7)

# ================= BROKERS DATABASE =================
BROKERS = {
    "vantage": {
        "name": "1️⃣ Vantage",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "USD: 161100 | EUR/GBP: 162204",
        "settings": "Platform: MT4/MT5, Standard / Raw Spread",
        "links": [
            ("🌐 Official Website Registration", "https://vigco.co/la-com-inv/nwYpA1xO"),
            ("📱 Telegram Mini App Registration", "https://t.me/vantagemarketsbot/VantageMiniAPP?startapp=d080fea26efa46a5b17bd2a3a2fe508b72d40aebd37b56ce9749f6b0fd21fa18"),
        ],
        "transfer_method": (
            "1. Vantage Portal / App login karein.\n"
            "2. Profile ➔ Transfer IB / CPA par jayein.\n"
            "3. Partnership Type: IB, IB Number: `161100` enter karein.\n"
            "4. Transfer Reason: 'Trading Education & Signals' likhein aur submit karein."
        )
    },
    "icmarkets": {
        "name": "2️⃣ IC Markets",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "80605",
        "settings": "Platform: MT4/MT5, Standard ya Raw Spread, Currency: USD",
        "links": [
            ("🌐 Register Link", "https://icmarkets.com/?camp=80605")
        ],
        "transfer_method": (
            "1. Live Chat ya Email (support@icmarkets.com) par contact karein.\n"
            "2. Request bhejein: 'Please transfer my trading account under Partner Code: 80605'."
        )
    },
    "exness": {
        "name": "3️⃣ Exness",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "jtz4pqy60n",
        "settings": "Platform: MT4/MT5, Account Type: Standard, Leverage: 1:2000, Currency: USD",
        "links": [
            ("🌐 Register Link", "https://one.exnesstrack.net/a/jtz4pqy60n")
        ],
        "transfer_method": (
            "1. Exness Personal Area mein Live Chat / Support Hub open karein.\n"
            "2. Partner Change request dalein aur Partner Code: `jtz4pqy60n` batayein.\n"
            "(Note: Agar transfer na ho sake to new email ID se new account banayein)."
        )
    },
    "hfm": {
        "name": "4️⃣ HFM (HF Markets)",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "384679",
        "settings": "Platform: MT4/MT5, Account Type: Pro, Leverage: 1:1000, Currency: USD",
        "links": [
            ("🌐 Register Link", "https://www.hfm.com/sv/en/?refid=384679")
        ],
        "transfer_method": (
            "(Existing profile transfer ki zaroorat nahi hai)\n"
            "1. HFM Members Area mein jayein ➔ Open New Trading Account par click karein.\n"
            "2. Account Type: Pro, Leverage: 1:1000 select karein.\n"
            "3. Introducing Broker ID / Campaign ID field mein code dalein: `384679`"
        )
    },
    "octa": {
        "name": "5️⃣ Octa (OctaFX)",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "17826811",
        "settings": "Platform: MT4/MT5, Real Account, Leverage: 1:500 ya 1:1000, Fixed Rate: OFF (Default), Currency: USD",
        "links": [
            ("🌐 Register Link", "https://my.octafx.com/open-account/?refid=ib17826811")
        ],
        "transfer_method": (
            "1. Direct Change IB Link par jayein:\n"
            "   https://my.octafx.com/change-partner-request/?partner=17826811\n"
            "2. Partner ID: `17826811` confirm karein.\n"
            "3. Reason: 'This IB provides guidance and help in trading. Signals and Trading Education.' submit karein."
        )
    },
    "xm": {
        "name": "6️⃣ XM Global",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "R88RG",
        "settings": "Platform: MT5, Account Type: Standard, Leverage: 1:1000, Currency: USD",
        "links": [
            ("🌐 Option 1 (Web)", "https://affs.click/rVEgV"),
            ("📈 Option 2 (Real Account)", "https://affs.click/mio5K"),
            ("📱 Option 3 (Mobile App)", "https://affs.click/53CQk"),
        ],
        "transfer_method": (
            "1. XM Members Area login karein.\n"
            "2. Create Additional Real Account par click karein.\n"
            "3. Jab pucha jaye 'Have a Partner Code?' to 'Enter Here' par click karke code dalein: `R88RG`"
        )
    },
    "justmarkets": {
        "name": "7️⃣ JustMarkets",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "29zk70kl3r",
        "settings": "Platform: MT4/MT5, Standard / Raw Spread, Currency: USD",
        "links": [
            ("🌐 Register Link", "https://one.justmarkets.link/a/29zk70kl3r/landing/scalping")
        ],
        "transfer_method": (
            "1. JustMarkets Live Chat par contact karein.\n"
            "2. Apna account IB Number: `29zk70kl3r` ke under link karne ki request karein."
        )
    },
    "puprime": {
        "name": "8️⃣ PU Prime",
        "min_dep": "$100 USD (Recommended $200+)",
        "ib_code": "15458577",
        "settings": "Platform: MT4/MT5, Standard / Prime, Currency: USD",
        "links": [
            ("🌐 Main Registration", "https://www.puprime.partners/?affid=MTU0NTg1Nzc="),
            ("📈 Open Trading Account", "https://www.puprime.partners/forex-trading-account/?affid=MTU0NTg1Nzc="),
            ("🤝 Sub-IB Registration", "https://www.puprimepartners.com/ib-registration/?affid=15458577"),
        ],
        "transfer_method": (
            "1. PU Prime Client Portal login karein.\n"
            "2. Profile ➔ Transfer IB / CPA par jayein (ya PU Prime support se contact karein).\n"
            "3. Partnership Type: IB, IB Number: `15458577` enter karke submit karein."
        )
    }
}

# ================= HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Welcome to Official IB VIP Access Portal!**\n\n"
        "📌 **Introducing Broker (IB) Program:**\n"
        "• **100% Free VIP Access:** Hamare Partner/IB code se link karne par broker apne standard spread/commission mein se share karta hai. Aapke liye **zero extra charges ya hidden fees** hain.\n"
        "• **Benefits:** Lifetime Free VIP Signals, Scalping Alerts, Dedicated Support, aur Daily Market Analysis.\n"
        "• **Minimum Deposit:** $100 USD ($200+ USD recommended behtar risk management ke liye).\n\n"
        "Neeche diye gaye buttons se apna Broker select karein ya verification form bharein:"
    )

    keyboard = [
        [InlineKeyboardButton("1️⃣ Vantage", callback_data="brk_vantage"), InlineKeyboardButton("2️⃣ IC Markets", callback_data="brk_icmarkets")],
        [InlineKeyboardButton("3️⃣ Exness", callback_data="brk_exness"), InlineKeyboardButton("4️⃣ HFM", callback_data="brk_hfm")],
        [InlineKeyboardButton("5️⃣ Octa", callback_data="brk_octa"), InlineKeyboardButton("6️⃣ XM Global", callback_data="brk_xm")],
        [InlineKeyboardButton("7️⃣ JustMarkets", callback_data="brk_justmarkets"), InlineKeyboardButton("8️⃣ PU Prime", callback_data="brk_puprime")],
        [InlineKeyboardButton("📋 7-Step Verification Flow", callback_data="flow_steps")],
        [InlineKeyboardButton("✅ Verify My Account (Submit Form)", callback_data="start_verification")]
    ]

    if update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    flow_text = (
        "📋 **Common 7-Step Verification Flow:**\n\n"
        "1. **Register Account:** Hamare referral link / partner code se account banayein.\n"
        "2. **KYC Verification:** Government ID / Passport submit karke broker profile verify karein.\n"
        "3. **Open Live MT4/MT5 Account:** Recommended settings ke sath new live account kholein.\n"
        "4. **Deposit Funds:** Minimum $100 USD deposit karein.\n"
        "5. **Submit Verification Form:** Bot mein 'Verify My Account' par click karke details aur screenshot submit karein.\n"
        "6. **Admin Approval:** Admin panel se verify hone ke baad access unlock hota hai.\n"
        "7. **Join Private Telegram Channel:** Lifetime private VIP channel access karein."
    )
    keyboard = [
        [InlineKeyboardButton("✅ Verify My Account Now", callback_data="start_verification")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_home")]
    ]
    await query.edit_message_text(flow_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def broker_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    broker_id = query.data.replace("brk_", "")
    b = BROKERS[broker_id]

    text = (
        f"🏦 **{b['name']}**\n\n"
        f"💵 **Minimum Deposit:** {b['min_dep']}\n"
        f"🔑 **Partner / IB Code:** `{b['ib_code']}`\n"
        f"⚙️ **Recommended Settings:** {b['settings']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🔄 **Existing Client Transfer Steps:**\n"
        f"{b['transfer_method']}\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )

    buttons = []
    for label, url in b["links"]:
        buttons.append([InlineKeyboardButton(label, url=url)])
    buttons.append([InlineKeyboardButton("✅ Verify This Account", callback_data="start_verification")])
    buttons.append([InlineKeyboardButton("⬅️ Back to All Brokers", callback_data="back_home")])

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

# ================= FORM CONVERSATION HANDLERS =================
async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Vantage", callback_data="sel_vantage"), InlineKeyboardButton("IC Markets", callback_data="sel_icmarkets")],
        [InlineKeyboardButton("Exness", callback_data="sel_exness"), InlineKeyboardButton("HFM", callback_data="sel_hfm")],
        [InlineKeyboardButton("Octa", callback_data="sel_octa"), InlineKeyboardButton("XM Global", callback_data="sel_xm")],
        [InlineKeyboardButton("JustMarkets", callback_data="sel_justmarkets"), InlineKeyboardButton("PU Prime", callback_data="sel_puprime")]
    ]
    await query.edit_message_text(
        "📝 **Verification Form (Step 1/6)**\n\nAapne kis Broker par account banaya ya transfer kiya hai?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return FORM_BROKER

async def form_broker_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["broker"] = query.data.replace("sel_", "").upper()
    await query.edit_message_text(
        f"Selected Broker: **{context.user_data['broker']}**\n\n"
        "👤 **Step 2/6:** Apna **Full Name (Trader Name)** likhein:"
    )
    return FORM_NAME

async def form_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("🌍 **Step 3/6:** Aapki **Country** ka naam likhein:")
    return FORM_COUNTRY

async def form_country_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    await update.message.reply_text("📧 **Step 4/6:** Broker par registered **Email Address** likhein:")
    return FORM_EMAIL

async def form_email_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("🔢 **Step 5/6:** Apna **Live Trading Account Number (MT4 / MT5)** enter karein:")
    return FORM_ACC_NUM

async def form_acc_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["acc_num"] = update.message.text
    await update.message.reply_text("💵 **Step 6/6:** Deposited Balance ($ USD) kitna hai?")
    return FORM_DEPOSIT

async def form_deposit_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deposit"] = update.message.text
    await update.message.reply_text(
        "📸 **Final Step:** Account Number aur Deposit proof ka **Screenshot Photo** attach karke bhejein:"
    )
    return FORM_SCREENSHOT

async def form_screenshot_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]
    tg_user = f"@{user.username}" if user.username else f"{user.first_name}"
    
    admin_summary = (
        "🚨 **Nayi IB Verification Request!**\n\n"
        f"🏦 **Broker:** {context.user_data['broker']}\n"
        f"👤 **Trader Name:** {context.user_data['name']}\n"
        f"🌍 **Country:** {context.user_data['country']}\n"
        f"📧 **Email:** {context.user_data['email']}\n"
        f"🔢 **Trading Account:** `{context.user_data['acc_num']}`\n"
        f"💵 **Deposited Balance:** ${context.user_data['deposit']}\n"
        f"📱 **Telegram:** {tg_user} (ID: `{user.id}`)"
    )

    admin_keyboard = [
        [
            InlineKeyboardButton("✅ Approve & Send VIP Link", callback_data=f"adm_app_{user.id}"),
            InlineKeyboardButton("❌ Reject Request", callback_data=f"adm_rej_{user.id}")
        ]
    ]

    # Admin chat par notification aur photo forward karna
    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=photo.file_id,
        caption=admin_summary,
        reply_markup=InlineKeyboardMarkup(admin_keyboard),
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "🎉 **Aapka Verification Form successfully submit ho gaya hai!**\n\n"
        "Hamari team details verify karne ke baad aapko isi bot par VIP Channel ka link send karegi (10-30 minutes).",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Process cancel kar diya gaya hai. Main menu ke liye /start type karein.")
    return ConversationHandler.END

# ================= ADMIN ACTIONS =================
async def admin_decision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    action = parts[1]
    client_id = int(parts[2])

    if action == "app":
        approval_msg = (
            "🎉 **Badhai Ho! Aapka Account Successfully Verify Ho Gaya Hai.**\n\n"
            f"Aapka VIP Access Unlock kar diya gaya hai:\n"
            f"🔗 **VIP Channel Link:** {VIP_CHANNEL_LINK}\n\n"
            "Channel join karein aur daily signals, scalping alerts aur market analysis ka fayda uthayein!"
        )
        await context.bot.send_message(chat_id=client_id, text=approval_msg, parse_mode="Markdown")
        await query.edit_message_caption(caption=f"{query.message.caption}\n\n✅ **STATUS: APPROVED BY ADMIN**")
    
    elif action == "rej":
        reject_msg = (
            "⚠️ **Verification Update:**\n\n"
            "Aapka trading account verify nahi ho saka. Sambhavit kaaran:\n"
            "• Account hamare Partner/IB code ke under link nahi hai.\n"
            "• Minimum deposit ($100) visible nahi hai.\n\n"
            "Kripya check karein ya dubara submit karne ke liye /start karein."
        )
        await context.bot.send_message(chat_id=client_id, text=reject_msg, parse_mode="Markdown")
        await query.edit_message_caption(caption=f"{query.message.caption}\n\n❌ **STATUS: REJECTED BY ADMIN**")

# ================= MAIN RUNNER =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(form_start, pattern="^start_verification$")],
        states={
            FORM_BROKER: [CallbackQueryHandler(form_broker_selected, pattern="^sel_")],
            FORM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_name_received)],
            FORM_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_country_received)],
            FORM_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_email_received)],
            FORM_ACC_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_acc_received)],
            FORM_DEPOSIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_deposit_received)],
            FORM_SCREENSHOT: [MessageHandler(filters.PHOTO, form_screenshot_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel_form)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^back_home$"))
    app.add_handler(CallbackQueryHandler(show_flow, pattern="^flow_steps$"))
    app.add_handler(CallbackQueryHandler(broker_details, pattern="^brk_"))
    app.add_handler(CallbackQueryHandler(admin_decision_handler, pattern="^adm_"))
    app.add_handler(conv_handler)

    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
