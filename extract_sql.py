
import re
def extract_sql(text):

    # Remove markdown
    text = text.replace("```sql", "")
    text = text.replace("```", "")

    # Match WITH ... ; OR SELECT ... ;
    match = re.search(
        r"((WITH[\s\S]*?;)|(SELECT[\s\S]*?;))",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return text.strip()
