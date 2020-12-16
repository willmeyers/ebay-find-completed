import typing

import lxml.html
import lxml.html.clean


class Element:
    cleaner = None

    def __init__(self, html_string: str, **cleaner_options):
        self.html_string = html_string
        self.element = lxml.html.fromstring(html_string)

        if cleaner_options:
            try:
                self.cleaner = lxml.html.clean.Cleaner(**cleaner_options)
            
            except Exception as err:
                raise err

    def clean(self) -> lxml.html.Element:
        """ Applys cleaner to element.
        """
        if self.cleaner:
            try:
                self.element = self.cleaner.clean_html(self.element)
            except Exception:
                pass

    def get(self, attribute_name: str) -> str:
        """ Returns an elements attribute if it exists.
        """
        attr = self.element.attrib.get(attribute_name)

        return attr

    def text(self) -> str:
        """ Returns the text content of the element.
        """
        text = self.element.text_content()

        return text
