""" Home App tests"""

from django.test import TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from .forms import SearchForm
from .models import Product, Category
from django.contrib.messages import get_messages
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# Create your tests here.
class HomeTests(TestCase):
    """ Unit Test Class for home function """

    def test_home_page(self):  # pragma: no cover
        """ Test of home view using verbal url """
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        """ Test of home view using reverse url """
        response = self.client.get(reverse("home:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class SearchTests(TestCase):
    """ Unit Test Class for search function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        Category.objects.create(name="test")
        category = Category.objects.get(name="test")
        for index in range(0, 9):
            Product.objects.create(
                name=f"My product {index}",
                category_id=category,
                nutriscore=index,
                url=f"www.test.fr {index}",
                ingredients="www.test.fr",
                photo="www.test.fr",
                fat_100g=0,
                saturate_fat_100g=0,
                salt_100g=0,
                sugars_100g=0,
                average_rating=0,
            )
        Product.objects.create(
            name=f"My product note",
            category_id=category,
            nutriscore=index,
            url=f"www.test_note.fr",
            ingredients="www.test_note.fr",
            photo="www.test_note.fr",
            fat_100g=0,
            saturate_fat_100g=0,
            salt_100g=0,
            sugars_100g=0,
            average_rating=5,
        )

    def test_search_page(self):  # pragma: no cover
        """ Test of search view using verbal url """
        response = self.client.post("/product/", {"search": "product"}, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        """ Test of search view using reverse url """
        response = self.client.post(
            reverse("home:search"), {"search": "product"}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_SearchForm_valid(self):  # pragma: no cover
        form = SearchForm(data={"search": "product!"})
        self.assertTrue(form.is_valid())
        text = form.cleaned_data["search"]
        self.assertEqual(text, "product")

    def test_SearchForm_invalid(self):  # pragma: no cover
        form = SearchForm(data={"search": ""})
        self.assertFalse(form.is_valid())

    def test_search_noresult(self):  # pragma: no cover
        response = self.client.post(
            reverse("home:search"), {"search": "dfsdfcds"}, follow=True
        )
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Il n'y a aucun résultat avec ces termes. Essayez encore !",
        )
        self.assertFalse(response.context["GoToProduct"])

    def test_search_result(self):  # pragma: no cover
        response = self.client.post(
            reverse("home:search"), {"search": "product"}, follow=True
        )
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"])

    def test_search_result_order_by_note(self):  # pragma: no cover
        response = self.client.post("/product/2/", {"search": "product"}, follow=True)
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"])

    def test_search_pagination(self):  # pragma: no cover
        response = self.client.post("/product/", {"search": "product"}, follow=True)
        response = self.client.get("/product/?page=2", {"page": "2"}, follow=True)
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"])

    def test_search_pagination_order_by_note(self):  # pragma: no cover
        response = self.client.post("/product/2/", {"search": "product"}, follow=True)
        response = self.client.get("/product/2/?page=2", {"page": "2"}, follow=True)
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"])


class SearchLiveTestCase(StaticLiveServerTestCase):
    def setUp(self):  # pragma: no cover

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(SearchLiveTestCase, self).setUp()

        Category.objects.create(name="test")
        category = Category.objects.get(name="test")
        for index in range(0, 9):
            Product.objects.create(
                name=f"My product {index}",
                category_id=category,
                nutriscore=index,
                url=f"www.test.fr {index}",
                ingredients="www.test.fr",
                photo="www.test.fr",
                fat_100g=0,
                saturate_fat_100g=0,
                salt_100g=0,
                sugars_100g=0,
                average_rating=0,
            )
        Product.objects.create(
            name=f"MyproductNote",
            category_id=category,
            nutriscore="a",
            url=f"www.test.fr",
            ingredients="www.test.fr",
            photo="www.test.fr",
            fat_100g=0,
            saturate_fat_100g=0,
            salt_100g=0,
            sugars_100g=0,
            average_rating=5,
        )

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(SearchLiveTestCase, self).tearDown()

    def test_search(self):  # pragma: no cover
        selenium = self.selenium
        selenium.get(f"{self.live_server_url}")
        selenium.maximize_window()
        text = selenium.find_element_by_class_name("main-search")
        submit = selenium.find_element_by_id("search-button")

        text.send_keys("product")

        #  submitting the form
        submit.click()

        assert "test" in selenium.page_source
        assert selenium.current_url == f"{self.live_server_url}/product/0/"
        assert selenium.find_element_by_xpath("//a[@href='?page=2']") is not None

        select = Select(selenium.find_element_by_class_name("order_product"))
        # select by visible text
        select.select_by_value("2")
        selenium.find_element_by_class_name("option2").click()

        divprod = selenium.find_element_by_class_name("products")
        element = divprod.find_element_by_class_name("product_MyproductNote")

        assert element is not None
