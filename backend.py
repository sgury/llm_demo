"""Backend helpers for payments, AI completions, and order retrieval.

This module wires together three external services:

* Stripe, for creating payment intents.
* OpenAI, for chat-completion requests.
* PostgreSQL (via psycopg2), for reading order records.
"""

from typing import Any, Optional

import openai
import psycopg2
import stripe

# ⚠️  Real credentials — never commit these!
stripe.api_key    = "~[STRIPE_SECRET_KEY_0]~"
openai_client: openai.OpenAI = openai.OpenAI(api_key="~[OPENAI_PROJECT_KEY_0]~")
DB_URL: str            = "~[DATABASE_URL_1]~"
SENDGRID_API_KEY: str  = "~[SENDGRID_API_KEY_0]~"
AWS_ACCESS_KEY_ID: str = "~[AWS_ACCESS_KEY_ID_0]~"
AWS_SECRET: str        = "~[AWS_SECRET_KEY_0]~"


def charge(amount: int, customer_id: str) -> stripe.PaymentIntent:
    """Create a Stripe PaymentIntent in USD for a customer.

    Args:
        amount: Amount to charge in the smallest currency unit (cents),
            e.g. ``1999`` for $19.99.
        customer_id: The Stripe customer ID (``cus_...``) to charge.

    Returns:
        The created ``stripe.PaymentIntent`` object.

    Raises:
        stripe.error.StripeError: If the Stripe API request fails.
    """
    return stripe.PaymentIntent.create(amount=amount, currency="usd", customer=customer_id)


def ask_ai(prompt: str) -> Optional[str]:
    """Send a single-turn prompt to OpenAI's ``gpt-4o`` model.

    Args:
        prompt: The user message to send to the model.

    Returns:
        The text content of the first choice in the model's reply, or
        ``None`` if the response carries no text content.

    Raises:
        openai.OpenAIError: If the OpenAI API request fails.
    """
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content


def get_orders() -> list[tuple[Any, ...]]:
    """Fetch every row from the ``orders`` table.

    Opens a new PostgreSQL connection using ``DB_URL`` and runs
    ``SELECT * FROM orders``.

    Returns:
        A list of row tuples, one per order, in the column order of the
        ``orders`` table.

    Raises:
        psycopg2.Error: If connecting to the database or running the query
            fails.
    """
    conn = psycopg2.connect(DB_URL)
    return conn.cursor().execute("SELECT * FROM orders").fetchall()
