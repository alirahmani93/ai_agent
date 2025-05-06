import datetime
import os
from zoneinfo import ZoneInfo

import resend
from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# def send_email(subject: str, content: str) -> dict:
#     resend.api_key = os.getenv("RESEND_API_KEY")
#     if not resend.api_key:
#         return {
#             "status": "error",
#             "error_message": "Resend API key is not set.",
#         }
#     params = {
#         "from": "Brainstorm Agent <agent@bitpin.ir>",
#         "to": ["ali.rahmani@bitpin.ir"],
#         "subject": subject,
#         "html": content
#     }
#
#     email_response = resend.Emails.send(params)
#     return {
#         "status": "success",
#         "report": f"Email sent successfully with ID: {email_response['id']}"
#     }


youtube_script_writer = Agent(
    name="youtube_script_writer",
    model="gemini-2.0-flash",
    instruction="You are a youtube script writer."
                "Based on the previous brainstorming conversation, you will write an amazing youtube script.",
    description="Writes a youtube script based on the previous brainstorming conversion.",
    tools=[]
)
root_agent = Agent(
    name="brainstorm_agent",
    model="gemini-2.0-flash",
    instruction=
        "Brainstorm with user and challenge their thoughts on the topic. Make sure you stay on topic and don't deviate from the topic and dont deviate from the topic."
        "You have specialized sub-agents:"
        "youtube_script_writer: Writes a youtube script based on the previous brainstorming conversation."
        "When user is done brainstorming, or you feel like you have enough information, you cab delegate the task to the youtube_script_writer sub-agent."
    ,
    description="you are a professional brainstorm agent.",
    tools=[],
    sub_agents=[youtube_script_writer]
)
