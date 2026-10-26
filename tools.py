# tools.py — Aliyu Saidu AI Agent Tools

# ----------------------------------------------------------------------
# Biographical & Professional Knowledge Base
# ----------------------------------------------------------------------
BIOGRAPHY_DATA = {
    "current_role": {
        "title": "Executive Director, Administration and Finance",
        "organization": "Kaduna Mining Development Company (KMDC)",
        "scope": "Oversees organizational performance, financial management, administrative efficiency, and strategic resource allocation.",
    },
    "past_roles": [
        {
            "title": "Pioneer Director-General",
            "organization": "Kaduna State Contributory Health Management Authority (KADCHMA)",
            "details": "Led the establishment, organizational rollout, and institutional development of Kaduna's contributory healthcare scheme.",
        },
        {
            "title": "Oversight and Validation Coordinator",
            "organization": "Subsidy Reinvestment and Empowerment Programme (SURE-P)",
            "unit": "Maternal and Child Health Unit",
        },
        {
            "title": "Administrative and ICT Officer",
            "organization": "National Identity Management Commission (NIMC)",
        },
        {
            "title": "Administrative and ICT Officer",
            "organization": "National Health Service (NHS), United Kingdom",
        },
    ],
    "education": [
        {
            "degree": "PhD in Public Health",
            "institution": "In Progress",
            "status": "Currently Pursuing",
        },
        {
            "degree": "Master of Science (MSc) in Health Informatics",
            "institution": "University of Leeds, United Kingdom",
        },
        {
            "degree": "Bachelor of Science (BSc) in Information Systems",
            "institution": "University of Leeds, United Kingdom",
        },
    ],
    "certifications": [
        "Leadership in Healthcare Management — Lagos Business School",
        "Performance-Based Health Financing",
        "NVQ Qualification in Health and Social Care — City & Guilds, UK",
    ],
    "politics": {
        "political_experience": "Contested on two occasions for Member of the Federal House of Representatives representing Igabi Federal Constituency.",
        "focus": "Democratic governance, legislative representation, public policy, and constituency development.",
    },
    "contact": {
        "email": "aliel_one@yahoo.com",
    },
}


def get_current_role_info():
    """Return details about Aliyu Saidu's current executive leadership position."""
    role = BIOGRAPHY_DATA["current_role"]
    return (
        f"Position: {role['title']}\n"
        f"Organization: {role['organization']}\n"
        f"Scope: {role['scope']}"
    )


def get_career_history(organization_keyword="all"):
    """
    Search or return Aliyu Saidu's full career background across public sector, health, and tech organizations.
    Accepts keywords like 'KADCHMA', 'SURE-P', 'NIMC', 'NHS', or 'all'.
    """
    keyword = organization_keyword.lower().strip()
    roles = BIOGRAPHY_DATA["past_roles"]

    if keyword == "all":
        output = ["Past Leadership & Administrative Roles:"]
        for r in roles:
            output.append(f"- {r['title']} at {r['organization']}")
        return "\n".join(output)

    matched = [
        f"- {r['title']} at {r['organization']}"
        for r in roles
        if keyword in r["organization"].lower() or keyword in r["title"].lower()
    ]
    if matched:
        return "\n".join(matched)
    return f"No specific career record found matching '{organization_keyword}'."


def get_academic_qualifications():
    """Return Aliyu Saidu's academic degrees and specialized professional qualifications."""
    output = ["Academic Qualifications:"]
    for edu in BIOGRAPHY_DATA["education"]:
        output.append(f"- {edu['degree']} ({edu['institution']})")

    output.append("\nProfessional Development & Certifications:")
    for cert in BIOGRAPHY_DATA["certifications"]:
        output.append(f"- {cert}")

    return "\n".join(output)


def get_political_engagement():
    """Return information on Aliyu Saidu's political leadership and legislative aspirations."""
    p = BIOGRAPHY_DATA["politics"]
    return f"Political Background: {p['political_experience']}\nFocus Areas: {p['focus']}"


def get_contact_information():
    """Return official contact email address for Aliyu Saidu."""
    return f"Official Contact Email: {BIOGRAPHY_DATA['contact']['email']}"


# ----------------------------------------------------------------------
# Tool Schemas for OpenAI Function Calling
# ----------------------------------------------------------------------
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_role_info",
            "description": "Get current executive role details for Aliyu Saidu at KMDC.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_career_history",
            "description": "Fetch past positions held by Aliyu Saidu (e.g., KADCHMA, SURE-P, NIMC, NHS UK).",
            "parameters": {
                "type": "object",
                "properties": {
                    "organization_keyword": {
                        "type": "string",
                        "description": "Organization filter such as 'KADCHMA', 'NHS', 'SURE-P', or 'all'.",
                    }
                },
                "required": ["organization_keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_academic_qualifications",
            "description": "Get academic degrees, universities attended, and professional certifications of Aliyu Saidu.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_political_engagement",
            "description": "Retrieve details on Aliyu Saidu's legislative contests and public governance engagement.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_contact_information",
            "description": "Get the official contact details for Aliyu Saidu.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


# ----------------------------------------------------------------------
# Tool Dispatcher
# ----------------------------------------------------------------------
def call_tool(name, args):
    if name == "get_current_role_info":
        return get_current_role_info()
    elif name == "get_career_history":
        return get_career_history(**args)
    elif name == "get_academic_qualifications":
        return get_academic_qualifications()
    elif name == "get_political_engagement":
        return get_political_engagement()
    elif name == "get_contact_information":
        return get_contact_information()
    return f"Unknown tool: {name}"


# --- quick test ---
if __name__ == "__main__":
    print(get_current_role_info())
    print("\n" + get_career_history("kadchma"))
    print("\n" + get_academic_qualifications())