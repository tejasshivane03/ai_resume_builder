"""
PDF generator service using Django templates and xhtml2pdf / WeasyPrint.
"""
from django.template.loader import render_to_string
import io
import logging

logger = logging.getLogger(__name__)


def generate_pdf(resume):
    """
    Render resume to PDF bytes.
    Tries xhtml2pdf first, then weasyprint, then returns rendered HTML in bytes as fallback.
    """
    template_name = f"resume/pdf/{resume.template or 'modern'}.html"
    context = {
        'resume': resume,
        'experience': resume.get_experience(),
        'education': resume.get_education(),
        'skills': resume.get_skills(),
        'projects': resume.get_projects(),
        'certifications': resume.get_certifications(),
    }

    try:
        html_string = render_to_string(template_name, context)
    except Exception as e:
        logger.error(f"Error rendering PDF template {template_name}: {e}")
        # fallback to modern template
        try:
            html_string = render_to_string('resume/pdf/modern.html', context)
        except Exception:
            return None

    # Method 1: Try xhtml2pdf
    try:
        from xhtml2pdf import pisa
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            return result.getvalue()
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"xhtml2pdf generation error: {e}")

    # Method 2: Try WeasyPrint
    try:
        from weasyprint import HTML
        return HTML(string=html_string).write_pdf()
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"WeasyPrint generation error: {e}")

    # Fallback: HTML printable bytes if no converter installed
    return html_string.encode('utf-8')
