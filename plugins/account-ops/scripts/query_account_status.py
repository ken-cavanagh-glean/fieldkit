#!/usr/bin/env python3
"""
Query Glean Account Status Agent for real-time account information.

Usage:
    python query_account_status.py "Snap"
    python query_account_status.py "Golden Gate Bridge"

Environment variables (or from .env file):
    GLEAN_API_TOKEN - Glean API token
    GLEAN_INSTANCE - Glean instance (default: scio-prod)

Agent returns:
    - Last meeting + Gong summary
    - Open to-dos from meetings/emails
    - Missed communications needing response
    - Internal flags from AE/DEM/Support
    - Hours used/remaining from Rocketlane
"""

import json
import os
import sys
from pathlib import Path
from glean.api_client import Glean


# Account Status Agent ID
AGENT_ID = "ccdc8e55722e48f98ef04d548f2b7e58"

# Potential .env file locations (checked in order)
ENV_FILE_PATHS = [
    Path.home() / "Desktop/lab/projects/QuestionMonitor/.env",
    Path.home() / "Desktop/lab/.env",
    Path.cwd() / ".env",
]


def load_env_file() -> None:
    """Load environment variables from .env file if not already set."""
    if os.getenv("GLEAN_API_TOKEN"):
        return  # Already set, skip

    for env_path in ENV_FILE_PATHS:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and not os.getenv(key):
                            os.environ[key] = value
            break  # Stop after first found .env


def query_account_status(account_name: str) -> dict:
    """Query the Account Status Agent for a given account."""

    # Try to load from .env if needed
    load_env_file()

    api_token = os.getenv("GLEAN_API_TOKEN")
    glean_instance = os.getenv("GLEAN_INSTANCE", "scio-prod")

    if not api_token:
        return {
            "error": "GLEAN_API_TOKEN environment variable required",
            "account": account_name
        }

    try:
        with Glean(api_token=api_token, instance=glean_instance) as client:
            # Call the agent
            run_response = client.client.agents.run(
                agent_id=AGENT_ID,
                input={
                    "question": f"Account Status for: {account_name}"
                }
            )

            # Extract answer from agent response
            answer_text = None
            sources = []

            if hasattr(run_response, 'messages') and run_response.messages:
                last_message = run_response.messages[-1]
                if hasattr(last_message, 'content'):
                    for block in last_message.content:
                        if hasattr(block, 'type') and block.type == 'text':
                            if hasattr(block, 'text'):
                                answer_text = block.text
                        # Extract sources if available
                        if hasattr(block, 'type') and block.type == 'sources':
                            if hasattr(block, 'sources'):
                                sources = [
                                    {"title": s.title, "url": s.url}
                                    for s in block.sources
                                    if hasattr(s, 'title') and hasattr(s, 'url')
                                ]

            if not answer_text:
                answer_text = str(run_response)

            return {
                "account": account_name,
                "status": answer_text,
                "sources": sources
            }

    except Exception as e:
        return {
            "error": str(e),
            "account": account_name
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python query_account_status.py <account_name>")
        print("Example: python query_account_status.py 'Snap'")
        sys.exit(1)

    account_name = sys.argv[1]
    result = query_account_status(account_name)

    # Output as JSON for easy parsing
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
