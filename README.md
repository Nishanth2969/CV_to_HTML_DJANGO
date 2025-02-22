# PDF to HTML CV Project

This Django project converts your PDF resume into a structured HTML page. If a PDF is uploaded, its content is extracted and displayed as HTML; if no PDF is present, a default static resume template is used. You can also upload a new PDF and remove the currently uploaded one.

## Features

- **PDF Extraction:**  
  Uses PyPDF2 to extract text from your uploaded PDF and post-processes it into headings, bullet lists, and paragraphs.

- **Dynamic vs. Static View:**  
  - **Dynamic View:** If a PDF is uploaded, its extracted content is displayed in HTML.
  - **Static View:** If no PDF exists, a default static resume template is shown.

- **File Upload & Removal:**  
  Provides an upload form to update your resume in PDF format and a button to remove the uploaded PDF.

- **Responsive UI:**  
  Styled with Bootstrap for a modern look.


## Usage

- **Dynamic Resume Display:**  
  If a PDF is present in the `resumes` folder (named `cv.pdf`), the project extracts its content and displays it in HTML on the resume page.

- **Static Resume Display:**  
  If no PDF is uploaded, a default static resume template (`static_cv.html`) is shown.

- **Upload a New PDF:**  
  If no PDF is uploaded (or after removing one), an upload form is displayed on the static template page. Use this form to upload your resume in PDF format.

- **Remove the Uploaded PDF:**  
  Click the “Remove PDF” button (available in the header) to delete the currently uploaded PDF and revert back to the static resume view.

## Technologies Used

- Django (3.2+)
- PyPDF2
- Bootstrap

