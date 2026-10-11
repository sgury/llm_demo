import openai
import stripe
import psycopg2

# ⚠️  Real credentials — never commit these!
stripe.api_key    = "~[STRIPE_SECRET_KEY_0]~"
openai_client     = openai.OpenAI(api_key="~[OPENAI_PROJECT_KEY_0]~")
DB_URL            = "~[DATABASE_URL_1]~"
SENDGRID_API_KEY  = "~[SENDGRID_API_KEY_0]~"
AWS_ACCESS_KEY_ID = "~[AWS_ACCESS_KEY_ID_0]~"
AWS_SECRET        = "~[AWS_SECRET_KEY_0]~"

def charge(amount, customer_id):
    return stripe.PaymentIntent.create(amount=amount, currency="usd", customer=customer_id)

def ask_ai(prompt):
    r = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def get_orders():
    conn = psycopg2.connect(DB_URL)
    return conn.cursor().execute("SELECT * FROM orders").fetchall()
