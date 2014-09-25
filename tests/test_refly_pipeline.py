import unittest
from refly_scraper.pipelines import ReflyPipeline
from refly_scraper.items import ReferenceItem
from refly_scraper.spiders.js import JsSpider

class ReflyPipelineTest(unittest.TestCase):
    def test_process_item(self):
        pipe = ReflyPipeline()
        item = ReferenceItem()
        item["name"] = "Math.cosh()"
        item["path"] = ['JavaScript', 'Standard Built-In objects', 'math']
        item["url"] = "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/cosh"
        item["content"] = "<h1>Hello World!</h1>"

        result = pipe.process_item(item, JsSpider())

        self.assertEqual(result["docset"], "JavaScript")
        self.assertEqual(result["name"], "Math.cosh()")
        self.assertEqual(result["type"], "method")
        self.assertEqual(result["parsed_url"], "/javascript/standard built-in objects/math/math.cosh()")
        self.assertEqual(result["parent"], "/javascript/standard built-in objects/math")
        self.assertEqual(result["content"], "# Hello World!\n\n")