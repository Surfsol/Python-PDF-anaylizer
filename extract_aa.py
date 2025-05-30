import subprocess

def extract_pdf_object_with_aa(pdf_path):
    try:
        result = subprocess.run(
            ['python', 'malware_detect/pdf-parser.py', pdf_path, '-s', '/AA'],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        object_ids = []

        for line in output.splitlines():
            if line.startswith('obj '):
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    object_ids.append(parts[1])

        return object_ids
    except Exception as e:
        return [f"Error running pdf-parser: {e}"]
