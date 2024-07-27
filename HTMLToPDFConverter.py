#this requires the machine to have command line tool - wkhtmltopdf
import pdfkit

WKHTMLTOPDF_LOCATION = ""

class HTMLToPDFConverter:
    def __init__(self, options = {
        "disable-external-links": True,
        "enable-javascript": True,
        "encoding": "UTF-8",
        'page-size': 'A3',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'no-outline': False
    }):
        self.options = options

    def convert(self,url,outputPDFName):
        pdfkit.from_url(url,outputPDFName,options=self.options)


#config_pdf = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_LOCATION)
#pdfkit.from_file(input=['h.html', 'w.html'], output_path='p2.pdf', configuration=config_pdf, options=options)

if __name__ == "__main__":
    htmlToPDFConverter= HTMLToPDFConverter()
    htmlToPDFConverter.convert("https://jira.atlassian.com/si/jira.issueviews:issue-html/JRASERVER-64028/JRASERVER-64028.html","Issue.pdf")