import string
from email import message_from_string
import re

non_ascii_list = {}

def is_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        print('ERRORRRRRR')
        return False

def non_ascii_fun(obj):
    print('in non 4444', obj)
    for key, value in obj.items():
        if isinstance(value, list):
            for i in value:
                if not is_ascii(i):
                    non_ascii_list[f"{key} [{i}]"] = value

        elif isinstance(value, str):
            if not is_ascii(value):
                non_ascii_list[key] = value
    return non_ascii_list

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

    # print("Return-Path", return_path.strip(),
    #     "From", from_field.strip(),
    #     "X-Originating-IP", x_origin_ip.strip(),
    #     "SPF", spf_result.group(1).strip() if spf_result else "Not found",
    #     "DKIM", dkim_result.group(1) if dkim_result else "Not found",
    #     "DMARC", dmarc_result.group(1) if dmarc_result else "Not found",
    #     "Received", [line.strip() for line in received_headers])

    return {
        "Return-Path": return_path.strip(),
        "From": from_field.strip(),
        "X-Originating-IP": x_origin_ip.strip(),
        "SPF": spf_result.group(1).strip() if spf_result else "Not found",
        "DKIM": dkim_result.group(1) if dkim_result else "Not found",
        "DMARC": dmarc_result.group(1) if dmarc_result else "Not found",
        "Received": [line.strip() for line in received_headers],
    }

# Example usage
if __name__ == "__main__":
    with open("header.txt", "r", encoding="utf-8") as f:
        raw_header = f.read()

    parsed = parse_headers(raw_header)
    for key, value in parsed.items():
        if key == "Received":
            print(f"\n{key} headers:")
            for i, line in enumerate(value, 1):
                print(f"  {i}. {line}")
        else:
            print(f"{key}: {value}")
