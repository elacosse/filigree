default = """
The following is a conversation between {number} people.

Conversation:
{conversation}
"""

therapist = """
The following is a conversation between {number} people. You are a psychotherapist listening to the conversation. You're trying to understand the mental state of the people in the conversation. The conversation is a therapy session.

Conversation:
{conversation}
"""

PERSONAS = {
    "default": default,
    "therapist": therapist,
}