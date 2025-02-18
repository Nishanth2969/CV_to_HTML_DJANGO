from django.shortcuts import render, redirect
import os
from django.conf import settings
import PyPDF2

# List of headings to be rendered as section titles.
HEADINGS = [
    "EDUCATION", "SKILLS", "ACHIEVEMENTS", "EXPERIENCE",
    "PROJECTS", "CONTACT", "PUBLICATIONS", "PATENTS",
    "SUMMARY", "ABOUT", "INTERESTS"
]

def cleanup_line(line):
    """
    Removes or replaces odd tokens that appear in extracted text.
    """
    line = line.replace("♂", "")
    line = line.replace("pen", "")  # remove extraneous prefixes from emails
    line = line.replace("/nishanthkotla", "")  # remove broken LinkedIn token
    line = line.replace("/Nishanth29", "")      # remove broken GitHub token
    return line.strip()

def bold_keywords(line):
    """
    Bold certain known entities (universities, companies, projects, etc.).
    Adjust the dictionary below as needed.
    """
    bold_map = {
        "New York University (NYU), Tandon School of Engineering": "<strong>New York University (NYU), Tandon School of Engineering</strong>",
        "Indian Institute of Technology Guwahati": "<strong>Indian Institute of Technology Guwahati</strong>",
        "Adobe": "<strong>Adobe</strong>",
        "Kaustubha Medtech Private Limited": "<strong>Kaustubha Medtech Private Limited</strong>",
        "HobbyHive": "<strong>HobbyHive</strong>",
        "Campus Trade Utopia: IITG Marketplace": "<strong>Campus Trade Utopia: IITG Marketplace</strong>",
    }
    for original, bolded in bold_map.items():
        if original in line:
            line = line.replace(original, bolded)
    return line

def merge_lines(text):
    """
    Merge broken lines into paragraphs.
    We assume that if a line does not end with punctuation (., !, ?, :)
    and the next line starts with a lowercase letter, it is a continuation.
    """
    lines = text.splitlines()
    merged = []
    buffer = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            # flush the buffer when an empty line is encountered
            if buffer:
                merged.append(buffer)
                buffer = ""
            merged.append("")  # preserve paragraph breaks
        else:
            if buffer:
                # if buffer does not end with punctuation and current line starts with lowercase, join
                if buffer[-1] not in ".!?:;" and stripped and stripped[0].islower():
                    buffer += " " + stripped
                else:
                    merged.append(buffer)
                    buffer = stripped
            else:
                buffer = stripped
    if buffer:
        merged.append(buffer)
    return merged

def format_extracted_text(pdf_text):
    """
    Convert raw PDF text into structured HTML.
    • First merges broken lines.
    • Skips unwanted lines (like the raw contact line starting with "Phone:").
    • Renders custom header lines ("Curriculum Vitae" and the name) with <h1>/<h2>.
    • Renders known section headings with <h3>.
    • Wraps bullet lines in lists, and everything else in <p>.
    """
    lines = merge_lines(pdf_text)
    processed_lines = []
    in_list = False

    for line in lines:
        # Clean up odd tokens and trim
        line = cleanup_line(line)

        # Skip a raw contact line if it starts with "Phone:"
        if line.lower().startswith("phone:"):
            continue

        # Render a custom header: if line equals "Curriculum Vitae" (case-insensitive)
        if line.strip().lower() == "curriculum vitae":
            processed_lines.append(f"<h1 class='text-center mt-3'>{line.strip()}</h1>")
            continue

        # Render the candidate's name specially (all uppercase)
        if line.strip() == "NISHANTH KOTLA":
            processed_lines.append(f"<h2 class='text-center mb-4'>{line.strip()}</h2>")
            continue

        # Bold known keywords in this line
        line = bold_keywords(line)

        # Check if the line is one of our known section headings
        if line.upper() in HEADINGS:
            if in_list:
                processed_lines.append("</ul>")
                in_list = False
            processed_lines.append(f"<h3 class='mt-4'>{line}</h3>")
        # Check if the line starts with a bullet or dash
        elif line.startswith("•") or line.startswith("-"):
            if not in_list:
                processed_lines.append("<ul>")
                in_list = True
            bullet_content = line.lstrip("•-").strip()
            processed_lines.append(f"<li>{bullet_content}</li>")
        else:
            if in_list:
                processed_lines.append("</ul>")
                in_list = False
            processed_lines.append(f"<p>{line}</p>")

    if in_list:
        processed_lines.append("</ul>")

    return "\n".join(processed_lines)

def cv_view(request):
    """
    Displays the CV.
    If a PDF exists in the resumes folder, its text is extracted, processed,
    and rendered via cv.html. Otherwise, static_cv.html is shown with an upload form.
    """
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'cv.pdf')
    
    # Handle file upload if form is submitted
    if request.method == "POST":
        if request.FILES.get('cv_pdf'):
            uploaded_file = request.FILES['cv_pdf']
            with open(pdf_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return redirect('cv')

    # If the PDF exists, extract and process its text
    if os.path.exists(pdf_path):
        pdf_text = ""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text + "\n"
        except Exception as e:
            pdf_text = f"An error occurred while processing the PDF: {e}"

        pdf_html = format_extracted_text(pdf_text)
        context = {'pdf_html': pdf_html}
        return render(request, 'cv_app/cv.html', context)
    else:
        return render(request, 'cv_app/static_cv.html', {'upload_form': True})

def remove_cv(request):
    """
    Deletes the uploaded cv.pdf file so you can revert to the static view.
    """
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'cv.pdf')
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    return redirect('cv')
