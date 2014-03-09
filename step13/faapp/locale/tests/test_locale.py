import unittest

from pyramid import testing
from faapp.locale import (
        add_renderer_globals,
        add_localizer,
        includeme,

    )

class PropertyHolder(object):
    """
        A class that holds any properties.
    """
    pass

class Test_add_renderer_globals(unittest.TestCase):
    def test_add_render_globals(self):
        req = PropertyHolder()
        req.translate = "translate"
        req.ungettext = "ungettext"
        req.localizer = "localizer"
        event = {
            "request": req,
        }
        add_renderer_globals(event)
        self.assertEqual(event["_"], "translate")
        self.assertEqual(event["ungettext"], "ungettext")
        self.assertEqual(event["localizer"], "localizer")

class Test_add_localizer(unittest.TestCase):
    def test_prepared_request(self):
        """
            Here we already have the localizer in the request.
        """
        req = PropertyHolder()
        req.localizer = "LOCALIZER"
        req.environ = {}
        event = PropertyHolder()
        event.request = req

        add_localizer(event)
        self.assertIs(event.request, req)
        self.assertEqual(req.localizer, "LOCALIZER")
        self.assertIn("translate", dir(req))
        self.assertIn("ungettext", dir(req))
        self.assertEqual(req.environ["fa.translate"], req.translate)

