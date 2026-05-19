import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'app.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS attack_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    how_to_identify TEXT NOT NULL,
    how_to_prevent TEXT NOT NULL,
    victim_steps TEXT NOT NULL,
    youtube_video_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    category TEXT NOT NULL
);
"""

ATTACK_TYPES = [
    {
        'slug': 'phishing',
        'name': 'Phishing',
        'description': 'Phishing is a cyberattack where attackers send fraudulent messages, typically via email, designed to trick victims into revealing sensitive information like passwords, credit card numbers, or personal data. These messages often impersonate trusted entities such as banks, tech companies, or government agencies.',
        'how_to_identify': '• Urgent or threatening language demanding immediate action\n• Suspicious sender email addresses with slight misspellings\n• Generic greetings like "Dear Customer" instead of your name\n• Links that don\'t match the claimed organization\'s domain\n• Requests for sensitive information via email\n• Poor grammar and spelling errors\n• Unexpected attachments',
        'how_to_prevent': '• Never click links in unsolicited emails — type URLs directly\n• Verify sender identity by contacting the organization directly\n• Enable multi-factor authentication on all accounts\n• Keep your email spam filters updated\n• Use anti-phishing browser extensions\n• Regularly update your software and operating system\n• Report suspicious emails to your IT department',
        'victim_steps': '• Change passwords immediately for any compromised accounts\n• Enable two-factor authentication everywhere possible\n• Contact your bank if financial information was shared\n• Run a full antivirus scan on your device\n• Monitor your accounts for unauthorized activity\n• Report the phishing attempt to the impersonated organization\n• File a report with your local cybercrime authority',
        'youtube_video_id': 'XBkzBrXlle0'
    },
    {
        'slug': 'spear_phishing',
        'name': 'Spear Phishing',
        'description': 'Spear phishing is a highly targeted form of phishing where attackers customize their fraudulent messages for a specific individual, organization, or role. Unlike generic phishing, spear phishing uses personal information gathered from social media, company websites, or data breaches to make the attack more convincing.',
        'how_to_identify': '• The email appears to come from a known colleague or superior\n• Contains specific personal or organizational details\n• Requests unusual actions like wire transfers or credential sharing\n• Creates a sense of urgency tied to a specific project or deadline\n• May reference real events or relationships within your organization\n• Slightly off email addresses mimicking real contacts',
        'how_to_prevent': '• Verify unusual requests through a separate communication channel\n• Limit personal information shared on social media\n• Implement email authentication protocols (SPF, DKIM, DMARC)\n• Train employees to recognize targeted attacks\n• Use advanced email filtering with AI-based detection\n• Establish verification procedures for financial transactions',
        'victim_steps': '• Immediately notify your IT security team\n• Change all potentially compromised passwords\n• Review recent account activity for unauthorized access\n• If financial data was shared, alert your bank immediately\n• Document the attack for forensic analysis\n• Warn colleagues who may be similarly targeted\n• Review and restrict your social media privacy settings',
        'youtube_video_id': 'N4OAUEtbMuE'
    },
    {
        'slug': 'smishing',
        'name': 'Smishing',
        'description': 'Smishing (SMS phishing) uses text messages to deceive victims into clicking malicious links, downloading harmful software, or revealing personal information. Attackers often impersonate banks, delivery services, or government agencies to create urgency and trick recipients into acting quickly.',
        'how_to_identify': '• Unexpected text messages from unknown numbers\n• Messages claiming your account has been compromised\n• Shortened URLs that hide the true destination\n• Requests to verify account information via text\n• Prize or lottery winning notifications you never entered\n• Package delivery notifications you weren\'t expecting\n• Messages with unusual urgency or time pressure',
        'how_to_prevent': '• Never click links in unexpected text messages\n• Don\'t reply to texts from unknown numbers\n• Contact organizations directly using their official number\n• Use your phone\'s built-in spam filtering\n• Install a reputable mobile security app\n• Never share personal information via text message\n• Block and report suspicious numbers',
        'victim_steps': '• Don\'t respond to the message further\n• Block the sender\'s number immediately\n• If you clicked a link, run a mobile security scan\n• Change passwords for any accounts you may have exposed\n• Contact your mobile carrier to report the smishing attempt\n• Monitor your bank and credit card statements\n• Report the message to your country\'s cybersecurity agency',
        'youtube_video_id': 'nRCFCt6cefs'
    },
    {
        'slug': 'vishing',
        'name': 'Vishing',
        'description': 'Vishing (voice phishing) is a social engineering attack conducted over phone calls. Attackers use voice communication to impersonate trusted entities like tech support, banks, or government agencies to manipulate victims into providing sensitive information or making payments.',
        'how_to_identify': '• Unexpected calls claiming to be from official organizations\n• Caller creates urgency or threatens consequences\n• Requests for sensitive information over the phone\n• Caller ID shows a spoofed or suspicious number\n• Pressure to make immediate decisions or payments\n• Offers that seem too good to be true\n• Caller refuses to let you call back on an official number',
        'how_to_prevent': '• Never share sensitive information over unsolicited calls\n• Hang up and call the organization\'s official number directly\n• Register your number on the Do Not Call list\n• Use call-blocking apps to filter suspicious numbers\n• Be skeptical of callers who create urgency\n• Verify caller identity before sharing any information\n• Educate family members about vishing tactics',
        'victim_steps': '• End the call immediately if you suspect vishing\n• Do not call back any number the attacker provided\n• Contact your bank if financial information was shared\n• Change passwords for any mentioned accounts\n• Report the call to your phone carrier\n• File a complaint with consumer protection agencies\n• Monitor your accounts for unusual activity',
        'youtube_video_id': 'sZ7bKEsr3Xk'
    },
    {
        'slug': 'baiting',
        'name': 'Baiting',
        'description': 'Baiting attacks lure victims with something enticing — a free download, a USB drive left in a public place, or a tempting offer. The bait contains malware or leads to credential theft. Unlike phishing, baiting relies on curiosity or greed rather than fear or urgency.',
        'how_to_identify': '• Found USB drives or storage devices in public spaces\n• Offers for free software, movies, or music downloads\n• Pop-up ads promising free gifts or prizes\n• Emails with enticing attachments from unknown senders\n• Websites offering "cracked" or pirated software\n• QR codes in suspicious or unusual locations\n• Too-good-to-be-true promotional offers',
        'how_to_prevent': '• Never plug unknown USB drives into your computer\n• Only download software from official sources\n• Use reputable antivirus software with real-time scanning\n• Be skeptical of free offers and prizes\n• Disable USB autorun on your devices\n• Report found storage devices to your IT department\n• Verify promotional offers through official channels',
        'victim_steps': '• Disconnect the infected device from the network immediately\n• Run a comprehensive antivirus scan\n• Change passwords on all accounts accessed from that device\n• Check for unauthorized software installations\n• Notify your IT department if it\'s a work device\n• Monitor for unusual account activity\n• Consider a full system restore if malware is found',
        'youtube_video_id': 'H06hLhBKMHc'
    },
    {
        'slug': 'pretexting',
        'name': 'Pretexting',
        'description': 'Pretexting involves an attacker creating a fabricated scenario (pretext) to gain a victim\'s trust and extract information. The attacker typically impersonates someone in authority — an IT administrator, auditor, co-worker, or law enforcement officer — and builds a believable backstory to justify their requests.',
        'how_to_identify': '• Someone you don\'t know asks for sensitive information with an elaborate backstory\n• The person claims authority but can\'t provide proper verification\n• Unusual requests for access, credentials, or personal data\n• The story seems designed to bypass normal security procedures\n• Pressure to help quickly due to an alleged emergency\n• Requests that skip normal verification channels',
        'how_to_prevent': '• Always verify the identity of people requesting sensitive information\n• Follow established verification procedures — no exceptions\n• Be cautious of unsolicited calls or visits from "authority figures"\n• Implement strict access control policies\n• Train staff to recognize pretexting scenarios\n• Require multi-person authorization for sensitive actions\n• Document and report unusual information requests',
        'victim_steps': '• Stop all communication with the suspected attacker\n• Report the incident to your security team immediately\n• Document everything you shared or disclosed\n• Change any credentials or access codes that were revealed\n• Alert colleagues who may be targeted next\n• Review access logs for unauthorized activity\n• Strengthen verification procedures based on the attack method',
        'youtube_video_id': 'qJb5sMFplvo'
    },
    {
        'slug': 'quid_pro_quo',
        'name': 'Quid Pro Quo',
        'description': 'Quid pro quo attacks involve an attacker offering something — typically a service or benefit — in exchange for information or access. Common examples include fake IT support offering to fix problems in exchange for login credentials, or surveys promising rewards for personal information.',
        'how_to_identify': '• Unsolicited offers of help, especially tech support\n• Someone asking for your password to "fix" a problem\n• Surveys or forms promising rewards for personal information\n• Callers offering free security audits or software upgrades\n• Requests for remote access to your computer\n• Offers that require you to disable security features\n• Help that requires sharing login credentials',
        'how_to_prevent': '• Never share passwords or credentials for "troubleshooting"\n• Only accept IT support through official channels\n• Be suspicious of unsolicited help offers\n• Verify the identity of anyone offering technical assistance\n• Don\'t disable security software at anyone\'s request\n• Report unsolicited support calls to your IT department\n• Use official support ticket systems for tech issues',
        'victim_steps': '• Revoke any remote access immediately\n• Change all passwords that were shared\n• Run a full security scan on your device\n• Report the incident to your IT department\n• Check for unauthorized software or changes\n• Monitor accounts for suspicious activity\n• Enable additional security measures on compromised accounts',
        'youtube_video_id': 'yyLLoNmR9SY'
    },
    {
        'slug': 'tailgating',
        'name': 'Tailgating',
        'description': 'Tailgating (also called piggybacking) is a physical social engineering attack where an unauthorized person follows an authorized individual into a restricted area. The attacker exploits social norms and politeness to gain physical access to buildings, server rooms, or other secured spaces.',
        'how_to_identify': '• Someone asks you to hold the door to a secure area\n• A person without visible credentials follows you through security\n• Unknown individuals in restricted areas without escort\n• People claiming to have forgotten their access badge\n• Delivery personnel requesting access without prior notification\n• Someone rushing to catch the door as it closes behind you\n• Unfamiliar faces in badge-required zones',
        'how_to_prevent': '• Never hold doors for unknown individuals in secure areas\n• Always verify the identity and credentials of visitors\n• Report tailgating attempts to security personnel\n• Use turnstiles or mantraps in high-security areas\n• Implement visitor management and escort policies\n• Train employees on physical security awareness\n• Install security cameras at all access points',
        'victim_steps': '• Alert security personnel immediately\n• Do not confront the unauthorized person directly\n• Note the person\'s description and where they went\n• Check if any sensitive areas were accessed\n• Review security camera footage\n• Report the incident through proper channels\n• Reinforce tailgating awareness with your team',
        'youtube_video_id': 'FhkP2-aGBss'
    }
]

QUIZ_QUESTIONS = [
    {
        'question': 'You receive an email from your bank asking you to click a link and verify your account details urgently. What should you do?',
        'option_a': 'Click the link and verify your details immediately',
        'option_b': 'Forward the email to friends for their opinion',
        'option_c': 'Contact your bank directly using their official phone number or website',
        'option_d': 'Reply to the email asking if it is legitimate',
        'correct_answer': 'C',
        'explanation': 'Never click links in unsolicited emails. Always contact your bank directly using known official contact information to verify any requests.',
        'category': 'phishing'
    },
    {
        'question': 'What is the primary difference between phishing and spear phishing?',
        'option_a': 'Spear phishing only uses phone calls',
        'option_b': 'Spear phishing targets specific individuals with personalized content',
        'option_c': 'Phishing is more dangerous than spear phishing',
        'option_d': 'There is no difference between them',
        'correct_answer': 'B',
        'explanation': 'Spear phishing is a targeted form of phishing that uses personal information about the victim to make the attack more convincing and harder to detect.',
        'category': 'spear_phishing'
    },
    {
        'question': 'You find a USB drive in the office parking lot. What should you do?',
        'option_a': 'Plug it into your computer to find the owner',
        'option_b': 'Give it to the receptionist to plug in and check',
        'option_c': 'Turn it in to your IT security team without plugging it in',
        'option_d': 'Throw it away since it\'s probably broken',
        'correct_answer': 'C',
        'explanation': 'Found USB drives may contain malware. This is a classic baiting attack. Always turn unknown devices over to your IT security team for safe analysis.',
        'category': 'baiting'
    },
    {
        'question': 'Someone calls claiming to be from IT support and asks for your password to fix a system issue. What should you do?',
        'option_a': 'Give them your password — IT needs it to fix problems',
        'option_b': 'Ask them to verify their identity and then share the password',
        'option_c': 'Hang up and contact IT support through your official company channels',
        'option_d': 'Share only your username, not your password',
        'correct_answer': 'C',
        'explanation': 'Legitimate IT support will never ask for your password. This is a common quid pro quo or vishing attack. Always verify through official channels.',
        'category': 'quid_pro_quo'
    },
    {
        'question': 'What is smishing?',
        'option_a': 'A phishing attack conducted through social media',
        'option_b': 'A phishing attack conducted through SMS text messages',
        'option_c': 'A phishing attack that uses smoke signals',
        'option_d': 'A type of malware that destroys data',
        'correct_answer': 'B',
        'explanation': 'Smishing (SMS + phishing) is a social engineering attack that uses text messages to trick victims into clicking malicious links or revealing personal information.',
        'category': 'smishing'
    },
    {
        'question': 'An unknown person in business attire asks you to hold the door to a restricted area, saying they forgot their badge. What should you do?',
        'option_a': 'Hold the door — they look professional',
        'option_b': 'Ask them to contact reception or security for temporary access',
        'option_c': 'Let them in but follow them to make sure they belong',
        'option_d': 'Ignore them completely and walk away',
        'correct_answer': 'B',
        'explanation': 'This is a tailgating attempt. Always direct unknown individuals to security or reception, regardless of their appearance. Never hold doors to restricted areas.',
        'category': 'tailgating'
    },
    {
        'question': 'Which of the following is a red flag in a potential phishing email?',
        'option_a': 'The email is from a known contact about a scheduled meeting',
        'option_b': 'The email contains a personalized greeting and correct spelling',
        'option_c': 'The sender\'s email domain doesn\'t match the organization they claim to represent',
        'option_d': 'The email was expected and relates to ongoing business',
        'correct_answer': 'C',
        'explanation': 'A mismatched sender domain is a strong indicator of phishing. Always check that the sender\'s email address matches the legitimate organization\'s domain.',
        'category': 'phishing'
    },
    {
        'question': 'What is pretexting in social engineering?',
        'option_a': 'Sending pre-written text messages to multiple targets',
        'option_b': 'Creating a fabricated scenario to gain trust and extract information',
        'option_c': 'Testing a system before it goes live',
        'option_d': 'Previewing text before sending it',
        'correct_answer': 'B',
        'explanation': 'Pretexting involves creating a false scenario or identity to manipulate victims into sharing information. The attacker builds a believable story to justify their requests.',
        'category': 'pretexting'
    },
    {
        'question': 'You receive a text message saying you\'ve won a $1000 gift card and need to click a link to claim it. What is this likely?',
        'option_a': 'A legitimate promotional offer',
        'option_b': 'A smishing (SMS phishing) attack',
        'option_c': 'A reminder from a store loyalty program',
        'option_d': 'A government notification about unclaimed funds',
        'correct_answer': 'B',
        'explanation': 'Unsolicited prize notifications via text message are almost always smishing attacks designed to steal your personal information or install malware.',
        'category': 'smishing'
    },
    {
        'question': 'What makes social engineering attacks particularly effective?',
        'option_a': 'They use the most advanced technology',
        'option_b': 'They exploit human psychology rather than technical vulnerabilities',
        'option_c': 'They can only target non-technical people',
        'option_d': 'They require expensive equipment to execute',
        'correct_answer': 'B',
        'explanation': 'Social engineering exploits human emotions like fear, trust, curiosity, and urgency. Technical defenses alone cannot prevent these attacks — awareness and training are essential.',
        'category': 'general'
    },
    {
        'question': 'A caller claims to be from a government tax agency, saying you owe back taxes and will be arrested if you don\'t pay immediately over the phone. What type of attack is this?',
        'option_a': 'Baiting',
        'option_b': 'Tailgating',
        'option_c': 'Vishing',
        'option_d': 'Smishing',
        'correct_answer': 'C',
        'explanation': 'This is a vishing (voice phishing) attack. Government agencies do not threaten arrest over the phone or demand immediate payment. Always hang up and contact the agency directly.',
        'category': 'vishing'
    },
    {
        'question': 'Which of the following is the BEST defense against social engineering attacks?',
        'option_a': 'Installing the most expensive antivirus software',
        'option_b': 'Regular security awareness training for all employees',
        'option_c': 'Using only Mac computers instead of Windows',
        'option_d': 'Avoiding the internet entirely',
        'correct_answer': 'B',
        'explanation': 'Security awareness training teaches people to recognize and respond to social engineering tactics, which is the most effective defense since these attacks target human behavior.',
        'category': 'general'
    },
    {
        'question': 'You receive a phone call from someone claiming to be your CEO, urgently requesting a wire transfer to a new vendor. What should you do?',
        'option_a': 'Process the transfer immediately — the CEO\'s request should be obeyed',
        'option_b': 'Ask the caller for the CEO\'s social security number to verify',
        'option_c': 'Verify the request through a separate communication channel before acting',
        'option_d': 'Forward the request to all employees for their input',
        'correct_answer': 'C',
        'explanation': 'This is likely a pretexting or spear phishing attack. Always verify unusual financial requests through a separate channel, such as calling the CEO\'s known phone number or asking in person.',
        'category': 'pretexting'
    },
    {
        'question': 'A website offers free premium software that normally costs $500, requiring only your email and password to download. What type of attack might this be?',
        'option_a': 'Tailgating',
        'option_b': 'Baiting',
        'option_c': 'Pretexting',
        'option_d': 'Vishing',
        'correct_answer': 'B',
        'explanation': 'This is a baiting attack that uses the lure of free valuable software to trick you into providing credentials or downloading malware.',
        'category': 'baiting'
    },
    {
        'question': 'What should you do if you suspect you\'ve already fallen victim to a phishing attack?',
        'option_a': 'Wait and see if anything bad happens',
        'option_b': 'Delete the phishing email and forget about it',
        'option_c': 'Immediately change your passwords, enable 2FA, and report the incident',
        'option_d': 'Create a new email account and abandon the old one',
        'correct_answer': 'C',
        'explanation': 'Immediate action is critical. Change passwords, enable two-factor authentication, monitor your accounts, and report the incident to your IT team and the impersonated organization.',
        'category': 'phishing'
    },
    {
        'question': 'Which of the following is an example of a quid pro quo attack?',
        'option_a': 'Receiving a threatening voicemail about taxes',
        'option_b': 'Finding a USB drive labeled "Confidential"',
        'option_c': 'Someone offering free tech support in exchange for your login credentials',
        'option_d': 'Following someone through a secured door',
        'correct_answer': 'C',
        'explanation': 'Quid pro quo means "something for something." The attacker offers a service (tech support) in exchange for valuable information (login credentials).',
        'category': 'quid_pro_quo'
    },
    {
        'question': 'Why is multi-factor authentication (MFA) important against social engineering?',
        'option_a': 'It makes your computer run faster',
        'option_b': 'It adds an extra layer of protection even if your password is compromised',
        'option_c': 'It prevents all types of cyberattacks completely',
        'option_d': 'It is only useful for social media accounts',
        'correct_answer': 'B',
        'explanation': 'MFA provides an additional verification step, so even if an attacker obtains your password through social engineering, they still cannot access your account without the second factor.',
        'category': 'general'
    },
    {
        'question': 'An email from a colleague contains an attachment you weren\'t expecting. The subject says "Check this out!" What should you do?',
        'option_a': 'Open the attachment — it\'s from a colleague',
        'option_b': 'Forward it to more colleagues to review',
        'option_c': 'Verify with the colleague through a separate channel before opening',
        'option_d': 'Download the attachment to your phone instead for safety',
        'correct_answer': 'C',
        'explanation': 'Even emails from known contacts can be spoofed or sent from compromised accounts. Always verify unexpected attachments through a different communication channel.',
        'category': 'spear_phishing'
    },
    {
        'question': 'What is the primary goal of most social engineering attacks?',
        'option_a': 'To destroy your computer hardware',
        'option_b': 'To gain unauthorized access to information, systems, or resources',
        'option_c': 'To slow down your internet connection',
        'option_d': 'To test your technical knowledge',
        'correct_answer': 'B',
        'explanation': 'Social engineering attacks aim to manipulate people into giving up confidential information, granting access to systems, or performing actions that benefit the attacker.',
        'category': 'general'
    },
    {
        'question': 'A delivery person you don\'t recognize asks to enter your office to deliver a package directly to a specific employee\'s desk. What should you do?',
        'option_a': 'Let them in — they have a package',
        'option_b': 'Accept the package at reception and deliver it yourself',
        'option_c': 'Ask them to leave the package at a different building',
        'option_d': 'Call the police immediately',
        'correct_answer': 'B',
        'explanation': 'This could be a tailgating attempt using a delivery pretext. Accept packages at a designated area and never allow unverified visitors into secure areas unescorted.',
        'category': 'tailgating'
    }
]


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript(SCHEMA)

    cursor.execute('SELECT COUNT(*) FROM attack_types')
    if cursor.fetchone()[0] == 0:
        for attack in ATTACK_TYPES:
            cursor.execute(
                'INSERT INTO attack_types (slug, name, description, how_to_identify, how_to_prevent, victim_steps, youtube_video_id) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (attack['slug'], attack['name'], attack['description'],
                 attack['how_to_identify'], attack['how_to_prevent'],
                 attack['victim_steps'], attack['youtube_video_id'])
            )

    cursor.execute('SELECT COUNT(*) FROM quiz_questions')
    if cursor.fetchone()[0] == 0:
        for q in QUIZ_QUESTIONS:
            cursor.execute(
                'INSERT INTO quiz_questions (question, option_a, option_b, option_c, option_d, correct_answer, explanation, category) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (q['question'], q['option_a'], q['option_b'], q['option_c'],
                 q['option_d'], q['correct_answer'], q['explanation'], q['category'])
            )

    conn.commit()
    conn.close()
    print(f'Database initialized at {DB_PATH}')
    print(f'  - {len(ATTACK_TYPES)} attack types seeded')
    print(f'  - {len(QUIZ_QUESTIONS)} quiz questions seeded')


if __name__ == '__main__':
    init_db()
