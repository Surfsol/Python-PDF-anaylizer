import streamlit as st
from email import message_from_string
import re


non_ascii_dict = {}

def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def non_ascii_fun(obj):
    checked = 0
    for key, value in obj.items():
        if isinstance(value, list):
            for i in value:
                checked += 1
                if not is_ascii(i):
                    non_ascii_dict[f"{key} [{i}]"] = value

        elif isinstance(value, str):
            checked += 1
            if not is_ascii(value):
                non_ascii_dict[key] = value
    if checked > 0 and len(non_ascii_dict) > 0:
        for field, content in non_ascii_dict.items():
            st.warning("🚨 Non-ASCII characters found in these fields:")
            st.code(f"{field}: {content}")
    elif checked > 0 and non_ascii_dict == {}:
        st.warning(f"✅ {checked} All characters are ASCII")
    return non_ascii_dict


def parse_sent_headers(sent_headers):
    """Extract email addresses from header like 'Name <email@example.com>' or just 'email@example.com'"""
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', sent_headers)
    email_obj = {}
    for i, mail in enumerate(emails, 1):
        email_obj[i] = mail
    return email_obj





def parse_headers(raw_headers):
    # Parse the raw header block
    msg = message_from_string(raw_headers)
    headers = dict(msg.items())

    # Extract key fields
    return_path = headers.get("Return-Path", "")
    from_field = headers.get("From", "")
    x_origin_ip = headers.get("X-Originating-IP", "")
    spf_result = re.search(r"Received-SPF:\s*(.*)", raw_headers)
    dkim_result = re.search(r"dkim=([a-z]+)", raw_headers)
    dmarc_result = re.search(r"dmarc=([a-z]+)", raw_headers)

    # Capture all Received headers (they can appear multiple times)
    received_headers = re.findall(r"Received: (.+?);", raw_headers, re.DOTALL)

    return {
        "Return-Path": return_path.strip(),
        "From": from_field.strip(),
        "X-Originating-IP": x_origin_ip.strip(),
        "SPF": spf_result.group(1).strip() if spf_result else "Not found",
        "DKIM": dkim_result.group(1) if dkim_result else "Not found",
        "DMARC": dmarc_result.group(1) if dmarc_result else "Not found",
        "Received": [line.strip() for line in received_headers],
    }
