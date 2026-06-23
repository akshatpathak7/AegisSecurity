import os
import csv
from collections import Counter

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'dataset.csv')
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))


def create_dataset():
    """Generate a labeled dataset of social engineering attack examples and safe messages."""
    data = []

    phishing_examples = [
        "Dear customer, your account has been compromised. Click here to verify your identity immediately.",
        "URGENT: Your PayPal account will be suspended unless you confirm your details within 24 hours.",
        "We detected unusual activity on your account. Please log in through this link to secure it.",
        "Your Apple ID was used to sign in on a new device. If this wasn't you, click here now.",
        "ALERT: Your bank account has been locked due to suspicious activity. Verify your identity here.",
        "Congratulations! You've been selected for a special reward. Click to claim your prize now.",
        "Your Netflix subscription payment failed. Update your billing information to avoid service interruption.",
        "Important security update: Your email password expires today. Click here to renew it.",
        "Dear valued customer, we need you to verify your account information to continue using our services.",
        "WARNING: Someone tried to access your account from an unknown location. Secure your account now.",
        "Your Amazon order #12345 cannot be delivered. Click here to update your shipping address.",
        "Action required: Your account verification is pending. Complete it within 48 hours or lose access.",
        "Urgent notice from your bank: Unusual transactions detected. Confirm your identity immediately.",
        "Your Microsoft account has been flagged for unusual activity. Sign in to review recent actions.",
        "Security alert: We noticed a login attempt from an unrecognized device. Was this you?",
        "Your password will expire in 24 hours. Click here to change it and avoid losing access.",
        "Dear user, your account has been temporarily restricted. Verify your identity to restore access.",
        "Important: Update your payment method to avoid disruption to your Google services.",
        "Your social security number has been compromised. Call this number immediately to protect yourself.",
        "Confirm your email address by clicking this link within 12 hours or your account will be deleted.",
        "Dear customer, we detected a fraudulent charge on your credit card. Click to dispute it now.",
        "Your package could not be delivered. Click this link to reschedule delivery and confirm your address.",
        "ATTENTION: Your tax refund is pending. Submit your bank details to receive your refund.",
        "Your iCloud storage is full. Click here to get free additional storage before your photos are deleted.",
        "Urgent: Your domain name is about to expire. Renew it now to avoid losing your website.",
    ]

    spear_phishing_examples = [
        "Hi John, as discussed in yesterday's meeting, please review the attached budget proposal and send your approval.",
        "Hey Sarah, Mark from finance asked me to forward you this invoice. Can you process the payment today?",
        "Following up on our conversation at the conference, I've attached the partnership proposal. Looking forward to your thoughts.",
        "Hi Mike, this is Lisa from HR. I need you to update your direct deposit information using this secure form.",
        "As per the CEO's request, please wire $50,000 to the following account for the vendor payment.",
        "Hi Jennifer, I'm from the London office. Could you send me the Q4 financial projections? James mentioned you'd have them.",
        "Dear Dr. Smith, regarding our collaboration on the research paper, please review the attached data and methodology.",
        "Hi team lead, the VP needs the employee salary spreadsheet by end of day. Can you send it to this address?",
        "Following our phone call, here are the merger documents. Please sign and return by Friday.",
        "Hi David, I'm the new contractor working with your team. Could you share the project repository access credentials?",
        "As we discussed in our Teams call, please transfer the funds to the new vendor account listed below.",
        "Hi, this is Tom from IT. We're migrating your department's accounts. I need your current login credentials to transfer your data.",
        "Dear Professor, a student recommended I reach out. Could you review my attached research proposal for the grant?",
        "Hi Alex, the board meeting has been moved up. Please share the confidential report with the new external auditor at this email.",
        "Following up from our LinkedIn conversation, I've attached the job offer letter. Please review and sign.",
    ]

    smishing_examples = [
        "USPS: Your package has been held due to incorrect address. Update here: bit.ly/track-pkg",
        "Your bank account shows suspicious activity. Verify now: trustbank-verify.com/secure",
        "Congrats! You won a $500 Walmart gift card. Claim before it expires: claim-gift.co/walmart",
        "IRS NOTICE: You have an outstanding tax balance. Pay immediately to avoid legal action: irs-pay.net",
        "Your Netflix account is on hold. Please verify your payment info: netflix-billing.co/update",
        "FedEx: Delivery attempted, no one home. Reschedule here: fedex-redeliver.com",
        "ALERT: Your credit card was charged $499.99. If unauthorized, click: verify-charge.com",
        "You have 1 new voicemail from an unknown number. Listen here: vm-listen.co/msg1234",
        "Your Venmo account requires verification. Tap to complete: venmo-verify.net/secure",
        "AMAZON: Your order #789 has been cancelled. Dispute this charge: amazon-help.co/dispute",
        "Free msg: Your phone bill is overdue. Pay now to avoid disconnection: phone-pay.net",
        "You're pre-approved for a $10,000 loan! Apply now with no credit check: easy-loan.co",
        "Your Apple ID has been disabled. Restore access: apple-restore.co/unlock",
        "Reminder: Your prescription is ready. Confirm pickup: rx-pickup.net/confirm",
        "Your social security benefits need updating. Verify your info: ssa-update.co",
    ]

    vishing_examples = [
        "Hello, this is the IRS calling. You owe back taxes and a warrant will be issued for your arrest unless you pay immediately.",
        "This is tech support from Microsoft. We've detected a virus on your computer. I need remote access to fix it.",
        "Hi, I'm calling from your bank's fraud department. We detected suspicious transactions. I need your account number to verify.",
        "This is an automated message from Social Security. Your number has been suspended due to suspicious activity. Press 1 now.",
        "Hello, I'm from your electric company. Your payment is overdue and service will be disconnected in one hour unless you pay now.",
        "This is a call from the police department. Your identity was used in a crime. Provide your details to clear your name.",
        "Hi, this is from Apple support. Your iCloud account has been breached. I need your password to secure it.",
        "Urgent call from your credit card company. Your card has been cloned. Give me the CVV to block it.",
        "This is the hospital calling. A family member has been in an accident. We need your insurance details immediately.",
        "Hello, I'm a representative from your internet provider. Your connection will be terminated unless you verify your account now.",
        "This is an emergency alert. Your bank account is being drained. Provide your PIN to freeze the account immediately.",
        "I'm calling from the lottery commission. You've won but we need your bank details to deposit the winnings.",
        "This is your company's IT department calling. We're doing emergency maintenance and need your VPN credentials.",
        "Hello, I'm from a charity helping disaster victims. Can you provide your credit card for a donation right now?",
        "This is a call from immigration services. Your visa status has issues. Provide personal details to resolve it now.",
    ]

    baiting_examples = [
        "FREE DOWNLOAD: Get the latest Adobe Photoshop Premium for free! No registration needed. Download now.",
        "Found USB drive labeled 'Confidential Salary Data 2024'. Contents unknown but potentially interesting.",
        "Download free Netflix premium accounts! Unlimited streaming. Just enter your email and password.",
        "Free Wi-Fi: Connect to 'FREE_PUBLIC_WIFI' for unlimited internet access. No password needed.",
        "Click here to download free antivirus software that will protect your computer from all threats.",
        "Free movie streaming: Watch any movie in HD for free. Just install our browser extension.",
        "Leaked database: Check if your password has been compromised. Enter your credentials to check.",
        "Free premium Spotify for life! Just download this app and log in with your Spotify credentials.",
        "USB drive found in lobby labeled 'Employee Bonuses Q4'. Plug in to see if your name is listed.",
        "Free VPN service: Browse anonymously with no speed limits. Download and install now.",
        "Get Microsoft Office for free! No subscription needed. Just download this cracked version.",
        "Free gaming cheats and hacks. Download our tool to get unlimited in-game currency.",
        "Exclusive leaked content available for free download. Click here before it gets taken down.",
        "Win a free iPhone 15! Just fill out this quick survey and download our app.",
        "Free online storage: Get 1TB of cloud storage free. Just create an account with your work email.",
    ]

    pretexting_examples = [
        "Hi, I'm the new IT auditor. I need to verify your system access credentials as part of the annual compliance review.",
        "I'm from the building management company. We need your office layout and security camera positions for fire safety compliance.",
        "Hello, I'm a researcher from the university conducting a study. I need access to your internal systems for academic purposes.",
        "I'm from corporate headquarters doing a surprise inspection. I need to see your access control systems and employee records.",
        "Hi, I'm your new insurance provider's representative. I need your employees' personal details to set up the new policy.",
        "I'm calling from the CEO's office. He's traveling and urgently needs the master password to access the system remotely.",
        "I'm from the health department conducting an investigation. I need access to your employee health records.",
        "Hello, I'm a journalist writing a story about your company. Can I see your internal communications for background?",
        "I'm the vendor for your new software. I need admin credentials to complete the installation remotely.",
        "Hi, this is the bank. We're updating our records and need to verify your company's financial details over the phone.",
        "I'm from law enforcement investigating a case. I need access to your security footage and employee records immediately.",
        "I'm the new cleaning service manager. I need keys to all offices and the alarm codes to set up the schedule.",
        "This is your accountant's office. We need your tax ID and bank routing numbers to file the quarterly returns.",
        "I'm from the phone company upgrading your lines. I need access to your server room to check the connections.",
        "Hello, I'm conducting a survey for a government agency. I need personal information about your household members.",
    ]

    quid_pro_quo_examples = [
        "I'm from IT support. I can fix that slow computer problem you've been having. Just give me your login credentials.",
        "Complete this security survey and receive a $100 Amazon gift card. We just need your personal details.",
        "Let me remote into your machine to install a free speed optimization tool. I just need your TeamViewer ID and password.",
        "I'll give you early access to the new company software if you share your admin credentials with me.",
        "Fill out this HR form to receive your annual bonus. We need your bank details and social security number.",
        "I can get you priority tech support if you give me your network access credentials.",
        "Share your login details and I'll set up the new email system for you right away, no waiting in the queue.",
        "I'll waive the service fee if you provide your account number and PIN right now over the phone.",
        "Participate in our beta testing program — we just need full system access to install the test version.",
        "I can unlock premium features on your account for free. Just verify your identity with your password.",
        "Let me check if your email has been hacked — just type your password into this verification tool.",
        "I'll process your refund faster if you confirm your credit card details over the phone right now.",
        "We'll give you a free security audit — just provide us remote access to your company network.",
        "Answer these questions and receive a free cybersecurity report. We need your company's network details.",
        "I'll expedite your support ticket if you share your screen and let me access your files directly.",
    ]

    tailgating_examples = [
        "Hey, can you hold the door? My hands are full with these boxes and I forgot my badge upstairs.",
        "I'm here for a meeting with the director but I left my visitor pass at the front desk. Can you let me in?",
        "Sorry, I'm the new intern and haven't received my access card yet. Could you badge me in?",
        "I'm the delivery guy — I need to bring this package directly to the 5th floor server room. Can you open the door?",
        "My badge isn't working, must be demagnetized. Can you swipe me into the secure area? I'm in a rush.",
        "I'm from the maintenance crew. We got called for an emergency repair. Mind letting me into the restricted wing?",
        "Could you hold the elevator? I need to get to the executive floor for an urgent meeting.",
        "I work in the other building but need to use your lab today. Can you let me in with your badge?",
        "I'm a contractor working on the HVAC system. My sponsor isn't here yet — can you let me into the building?",
        "Hey colleague, I left my badge in my car and I'm late for a meeting. Can you swipe me in?",
        "I'm from the catering company setting up for the event. Can you let us into the conference area?",
        "My card reader seems broken. I've been working here for years, you've seen me around. Just let me in.",
        "I need to deliver these flowers to someone on the 3rd floor. Can you hold the security door?",
        "I'm the new cleaning staff. My supervisor was supposed to give me a badge but hasn't yet. Can I follow you in?",
        "I left my wallet with my badge inside at my desk. Can you please let me back into the office?",
    ]

    safe_examples = [
        "Hi team, the meeting has been rescheduled to 3 PM tomorrow. Please update your calendars.",
        "Please find attached the Q3 report as discussed. Let me know if you have any questions.",
        "Reminder: The office will be closed next Monday for the holiday. Enjoy the long weekend!",
        "Your Amazon order #456789 has been shipped and will arrive by Thursday.",
        "Hi Mom, just checking in. How was your doctor's appointment today?",
        "The weekly team standup is at 9 AM. Please prepare your status updates.",
        "Your flight confirmation: Departure at 8:15 AM from Terminal 2, Gate B7.",
        "Happy birthday! Wishing you a wonderful year ahead.",
        "The quarterly town hall is scheduled for Friday at 2 PM in the main auditorium.",
        "Your subscription renewal was successful. Thank you for being a valued customer.",
        "Meeting notes from today's discussion are attached. Action items are highlighted.",
        "The company picnic is this Saturday at Central Park. Families are welcome!",
        "Please review the attached design mockups and share your feedback by Wednesday.",
        "Your password was successfully changed. If you did not make this change, contact support.",
        "Lunch order for tomorrow: Please reply with your choice from the attached menu.",
        "The project deadline has been extended to next Friday. Please adjust your timelines accordingly.",
        "New parking permits are available at the front desk. Please pick yours up by end of week.",
        "Great job on the presentation today! The client was very impressed with our proposal.",
        "Reminder: Annual performance reviews are due by the end of this month.",
        "The office kitchen will be cleaned this Thursday. Please remove personal items from the fridge.",
        "Your library book is due for return on March 15th. You can renew it online.",
        "The gym class schedule has been updated. Check the app for new time slots.",
        "Congratulations on completing the training course! Your certificate is attached.",
        "The network will undergo maintenance this weekend. Expect brief interruptions.",
        "Please RSVP for the team dinner by Wednesday so we can make a reservation.",
        "Your dentist appointment is confirmed for Tuesday at 10 AM.",
        "The new coffee machine has been installed in the break room. Enjoy!",
        "Thanks for your feedback on the proposal. I've incorporated your suggestions.",
        "The company newsletter for this month is ready. Check your inbox.",
        "Your car insurance policy renewal documents are attached for your review.",
        "Hi, just wanted to share these vacation photos from our trip. Hope you enjoy them!",
        "The weekly grocery list is on the fridge. Can you pick up milk on your way home?",
        "Your gym membership has been renewed. Your new card is available at the front desk.",
        "School is closed tomorrow due to a snow day. Kids will have a remote learning day.",
        "The book club meets this Thursday at 7 PM. We're discussing the latest chapter.",
        "Your appointment with Dr. Johnson has been confirmed for Friday at 3 PM.",
        "The community volunteer event is this Saturday. Sign up at the community center.",
        "Thank you for your purchase. Your receipt and warranty information are attached.",
        "The neighborhood association meeting is next Tuesday at 6:30 PM in the community hall.",
        "Your phone plan has been updated. View your new plan details in the app.",
    ]

    for text in phishing_examples:
        data.append({'text': text, 'label': 'phishing'})
    for text in spear_phishing_examples:
        data.append({'text': text, 'label': 'spear_phishing'})
    for text in smishing_examples:
        data.append({'text': text, 'label': 'smishing'})
    for text in vishing_examples:
        data.append({'text': text, 'label': 'vishing'})
    for text in baiting_examples:
        data.append({'text': text, 'label': 'baiting'})
    for text in pretexting_examples:
        data.append({'text': text, 'label': 'pretexting'})
    for text in quid_pro_quo_examples:
        data.append({'text': text, 'label': 'quid_pro_quo'})
    for text in tailgating_examples:
        data.append({'text': text, 'label': 'tailgating'})
    for text in safe_examples:
        data.append({'text': text, 'label': 'safe'})

    return data


def train_model():
    print("Creating dataset...")
    records = create_dataset()
    texts = [record['text'] for record in records]
    labels = [record['label'] for record in records]

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', newline='', encoding='utf-8') as dataset_file:
        writer = csv.DictWriter(dataset_file, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(records)

    label_distribution = Counter(labels)
    distribution_text = "\n".join(
        f"{label}: {count}" for label, count in label_distribution.most_common()
    )
    print(f"Dataset saved: {len(records)} samples")
    print(f"Label distribution:\n{distribution_text}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print("Training TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=1
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression classifier...")
    model = LogisticRegression(
        max_iter=1000,
        C=10,
        class_weight='balanced',
        random_state=42
    )
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    train_accuracy = model.score(X_train_tfidf, y_train)
    test_accuracy = model.score(X_test_tfidf, y_test)
    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")

    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    vectorizer_path = os.path.join(MODEL_DIR, 'vectorizer.pkl')

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"\nModel saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")


if __name__ == '__main__':
    train_model()
