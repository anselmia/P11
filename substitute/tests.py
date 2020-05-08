import time
import json
from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from account.models import User
from home.models import Product, Category, Rating
from .models import Substitute
from django.contrib.messages import get_messages
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.db.transaction import atomic


# Create your tests here.
# class SubstituteTests(TestCase):
#     def setUp(self):  # pragma: no cover
#         Category.objects.create(name="test")
#         Category.objects.create(name="test_test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#                 average_rating=0,
#             )
#         category_2 = Category.objects.get(name="test_test")
#         Product.objects.create(
#             name=f"test",
#             category_id=category_2,
#             nutriscore="a",
#             url=f"www.test.fra",
#             ingredients="www.test.fra",
#             photo="www.test.fra",
#             fat_100g=0,
#             saturate_fat_100g=0,
#             salt_100g=0,
#             sugars_100g=0,
#             average_rating=5,
#         )

#     def test_substitute_page(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             "/substitute/" + str(product.id) + "/", args=(product.id,), follow=True
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_view(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
#         )
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "substitute.html")

#     def test_search_noresult(self):  # pragma: no cover
#         product = Product.objects.get(name="test")
#         response = self.client.get(
#             reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
#         )
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Il n'y a pas de substitut pour ce produit")

#     def test_search_result(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         self.assertTrue(response.context["substitutes"])
#         substitutes = response.context["substitutes"]
#         self.assertTrue(len(substitutes) > 0)

#     def test_search_result_order_by_note(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             "/substitute/" + str(product.id) + "/2/", follow=True
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         self.assertTrue(response.context["substitutes"])
#         substitutes = response.context["substitutes"]
#         self.assertTrue(len(substitutes) > 0)

#     def test_search_pagination(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
#         )
#         response = self.client.get(
#             reverse("substitute:search-a-substitute", args=(product.id,)),
#             {"page": "2"},
#             follow=True,
#         )
#         self.assertTrue(response.context["product"])
#         self.assertTrue(response.context["substitutes"])
#         substitutes = response.context["substitutes"]
#         self.assertTrue(len(substitutes) > 0 and len(substitutes) < 6)

#     def test_search_pagination_order_by_note(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             "/substitute/" + str(product.id) + "/2/", follow=True
#         )
#         response = self.client.get(
#             "/substitute/" + str(product.id) + "/2/", {"page": "2"}, follow=True,
#         )
#         self.assertTrue(response.context["product"])
#         self.assertTrue(response.context["substitutes"])
#         substitutes = response.context["substitutes"]
#         self.assertTrue(len(substitutes) > 0 and len(substitutes) < 6)


# class SubstituteLiveTestCase(StaticLiveServerTestCase):
#     def setUp(self):  # pragma: no cover
#         ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
#         self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
#         super(SubstituteLiveTestCase, self).setUp()
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#                 average_rating=0,
#             )
#         Product.objects.create(
#             name=f"MyproductNote",
#             category_id=category,
#             nutriscore="a",
#             url=f"www.test.fr",
#             ingredients="www.test.fr",
#             photo="www.test.fr",
#             fat_100g=0,
#             saturate_fat_100g=0,
#             salt_100g=0,
#             sugars_100g=0,
#             average_rating=5,
#         )

#     def tearDown(self):  # pragma: no cover
#         self.selenium.quit()
#         super(SubstituteLiveTestCase, self).tearDown()

#     def test_substitute(self):  # pragma: no cover
#         selenium = self.selenium
#         product = Product.objects.get(name="My product 1")
#         selenium.get(f"{self.live_server_url}")
#         selenium.maximize_window()
#         selenium.implicitly_wait(5)

#         text = selenium.find_element_by_class_name("main-search")
#         submit = selenium.find_element_by_id("search-button")
#         text.send_keys("product")
#         submit.click()
#         wait = WebDriverWait(selenium, 20)
#         wait.until(EC.url_to_be(f"{self.live_server_url}/product/0/"))

#         product_1 = selenium.find_element_by_xpath(
#             f"//a[@href='/substitute/{product.id}/']"
#         )
#         while selenium.current_url == f"{self.live_server_url}/product/0/":
#             product_1.click()

#         time.sleep(10)

#         current_url = selenium.current_url
#         if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
#             current_url = selenium.current_url[:-1]

#         assert current_url == f"{self.live_server_url}/substitute/{str(product.id)}"
#         assert selenium.find_element_by_xpath("//a[@href='?page=2']") is not None
#         assert "Vous pouvez remplacez cet aliment par :" in selenium.page_source

#         select = Select(selenium.find_element_by_class_name("order_substitute"))
#         # select by visible text
#         select.select_by_value("2")
#         selenium.find_element_by_class_name("option2").click()

#         divprod = selenium.find_element_by_class_name("substitutes")
#         element = divprod.find_element_by_class_name("substitute_MyproductNote")

#         assert element is not None


# class DetailTests(TestCase):
#     def setUp(self):  # pragma: no cover
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )
#         self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
#         User.objects.create_user(**self.credentials)
#         self.client.login(
#             username=self.credentials["username"], password=self.credentials["password"]
#         )

#     def test_detail_page(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             "/detail/" + str(product.id) + "/" + str(substitute.id),
#             args=(product.id, substitute.id,),
#             follow=True,
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_view(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
#         )
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "detail.html")

#     def test_detail_no_result(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         response = self.client.get(
#             reverse("substitute:detail", args=(product.id, 13,)), follow=True
#         )
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(
#             str(messages[0]),
#             "Il y a eu une lors de la récupération des information du substitut",
#         )
#         self.assertTemplateUsed(response, "home.html")

#     def test_detail_result(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         substitute = response.context["substitute"]
#         self.assertEqual(substitute.name, "My product 2")
#         self.assertTemplateUsed(response, "detail.html")
#         self.assertFalse(response.context["exist"])

#     def test_detail_favoris_exist(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         user = User.objects.get(username="testuser")
#         Substitute.objects.create(
#             product_id=product, substitute_id=substitute, user_id=user
#         )
#         response = self.client.get(
#             reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         product = response.context["substitute"]
#         self.assertEqual(product.name, "My product 2")
#         self.assertTemplateUsed(response, "detail.html")
#         self.assertTrue(response.context["exist"])


# class DetailLiveTestCase(StaticLiveServerTestCase):
#     def setUp(self):  # pragma: no cover
#         ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
#         self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
#         super(DetailLiveTestCase, self).setUp()
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )

#     def tearDown(self):  # pragma: no cover
#         self.selenium.quit()
#         super(DetailLiveTestCase, self).tearDown()

#     def test_detail(self):  # pragma: no cover
#         selenium = self.selenium
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         find_url = f"{reverse('substitute:search-a-substitute', kwargs={'product_id':product.id})}"
#         selenium.get(self.live_server_url + find_url)
#         selenium.maximize_window()
#         selenium.implicitly_wait(5)

#         substitute_a = selenium.find_element_by_xpath(
#             f"//a[@href='/detail/{product.id}/{substitute.id}/']"
#         )
#         while (
#             selenium.current_url
#             == f"{self.live_server_url}/substitute/{str(product.id)}/"
#         ):
#             substitute_a.click()

#         current_url = selenium.current_url
#         if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
#             current_url = selenium.current_url[:-1]
#         assert (
#             current_url
#             == f"{self.live_server_url}/detail/{str(product.id)}/{str(substitute.id)}"
#         )
#         assert "Fiche d'OpenFoodFacts" in selenium.page_source
#         assert (
#             "Vous devez vous connecter pour enregistrer ce substitut"
#             in selenium.page_source
#         )


# class SaveTests(TestCase):
#     def setUp(self):  # pragma: no cover
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )
#         self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
#         User.objects.create_user(**self.credentials)
#         self.client.login(
#             username=self.credentials["username"], password=self.credentials["password"]
#         )

#     def test_save_page(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             "/save/" + str(product.id) + "/" + str(substitute.id),
#             args=(product.id, substitute.id,),
#             follow=True,
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_view(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:save", args=(product.id, substitute.id,)), follow=True
#         )
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "detail.html")

#     def test_save(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:save", args=(product.id, substitute.id,)), follow=True
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         substitute = response.context["substitute"]
#         self.assertEqual(substitute.name, "My product 2")
#         self.assertTemplateUsed(response, "detail.html")
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Votre substitut a été sauvé")
#         user = User.objects.get(username="testuser")
#         self.assertTrue(
#             Substitute.objects.filter(
#                 product_id=product, substitute_id=substitute, user_id=user
#             ).exists()
#         )


# class SaveLiveTestCase(StaticLiveServerTestCase):
#     def setUp(self):  # pragma: no cover
#         self.credentials = {
#             "username": "usertest",
#             "password": "!!!!!!!!",
#             "email": "test_test@test.fr",
#         }
#         User.objects.create_user(**self.credentials)
#         ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
#         self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
#         super(SaveLiveTestCase, self).setUp()
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )

#         # Login the user
#         self.assertTrue(
#             self.client.login(
#                 username=self.credentials["username"],
#                 password=self.credentials["password"],
#             )
#         )
#         # Add cookie to log in the browser
#         cookie = self.client.cookies["sessionid"]
#         self.selenium.get(
#             self.live_server_url
#         )  # visit page in the site domain so the page accepts the cookie
#         self.selenium.add_cookie(
#             {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
#         )

#     def tearDown(self):  # pragma: no cover
#         self.selenium.quit()
#         super(SaveLiveTestCase, self).tearDown()

#     def test_save(self):  # pragma: no cover
#         selenium = self.selenium
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         find_url = f"{reverse('substitute:detail',kwargs={'product_id':product.id, 'substitute_id':substitute.id})}"
#         selenium.get(self.live_server_url + find_url)
#         selenium.maximize_window()
#         selenium.implicitly_wait(5)

#         save = selenium.find_element_by_xpath(
#             f"//a[@href='/save/{product.id}/{substitute.id}/']"
#         )
#         save.click()
#         current_url = selenium.current_url
#         if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
#             current_url = selenium.current_url[:-1]

#         assert (
#             current_url
#             == f"{self.live_server_url}/save/{str(product.id)}/{str(substitute.id)}"
#         )
#         assert "Votre substitut a été sauvé" in selenium.page_source
#         user = User.objects.get(username="usertest")
#         assert Substitute.objects.filter(
#             product_id=product, substitute_id=substitute, user_id=user
#         ).exists()


# class DetailFavorisTests(TestCase):
#     def setUp(self):  # pragma: no cover
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )
#         self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
#         User.objects.create_user(**self.credentials)
#         self.client.login(
#             username=self.credentials["username"], password=self.credentials["password"]
#         )
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         user = User.objects.get(username="testuser")
#         Substitute.objects.create(
#             product_id=product, substitute_id=substitute, user_id=user
#         )

#     def test_DetailFavoris_page(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             "/detail_favoris/" + str(product.id) + "/" + str(substitute.id),
#             args=(product.id, substitute.id,),
#             follow=True,
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_view(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:detail_favoris", args=(product.id, substitute.id,)),
#             follow=True,
#         )
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "detail_favoris.html")

#     def test_detail_favoris(self):  # pragma: no cover
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         response = self.client.get(
#             reverse("substitute:detail_favoris", args=(product.id, substitute.id,)),
#             follow=True,
#         )
#         product = response.context["product"]
#         self.assertEqual(product.name, "My product 1")
#         substitute = response.context["substitute"]
#         self.assertEqual(substitute.name, "My product 2")
#         self.assertTemplateUsed(response, "detail_favoris.html")


# class DetailFavorisLiveTestCase(StaticLiveServerTestCase):
#     def setUp(self):  # pragma: no cover
#         self.credentials = {
#             "username": "usertest",
#             "password": "!!!!!!!!",
#             "email": "test_test@test.fr",
#         }
#         User.objects.create_user(**self.credentials)
#         ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
#         self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
#         super(DetailFavorisLiveTestCase, self).setUp()
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 9):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#             )

#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         user = User.objects.get(username="usertest")
#         Substitute.objects.create(
#             product_id=product, substitute_id=substitute, user_id=user
#         )
#         # Login the user
#         self.assertTrue(
#             self.client.login(
#                 username=self.credentials["username"],
#                 password=self.credentials["password"],
#             )
#         )
#         # Add cookie to log in the browser
#         cookie = self.client.cookies["sessionid"]
#         self.selenium.get(
#             self.live_server_url
#         )  # visit page in the site domain so the page accepts the cookie
#         self.selenium.add_cookie(
#             {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
#         )

#     def tearDown(self):  # pragma: no cover
#         self.selenium.quit()
#         super(DetailFavorisLiveTestCase, self).tearDown()

#     def test_save(self):  # pragma: no cover
#         selenium = self.selenium
#         product = Product.objects.get(name="My product 1")
#         substitute = Product.objects.get(name="My product 2")
#         selenium.get(f"{self.live_server_url}/favorites")
#         selenium.maximize_window()
#         selenium.implicitly_wait(5)

#         details_favoris = selenium.find_element_by_xpath(
#             f"//a[@href='/detail_favoris/{product.id}/{substitute.id}/']"
#         )
#         while selenium.current_url == f"{self.live_server_url}/favorites/":
#             details_favoris.click()
#         current_url = selenium.current_url
#         if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
#             current_url = selenium.current_url[:-1]

#         assert (
#             current_url
#             == f"{self.live_server_url}/detail_favoris/{str(product.id)}/{str(substitute.id)}"
#         )
#         assert "Détails du favoris" in selenium.page_source


# class RatingTests(TestCase):
#     def setUp(self):  # pragma: no cover
#         Category.objects.create(name="test")
#         category = Category.objects.get(name="test")
#         for index in range(0, 3):
#             Product.objects.create(
#                 name=f"My product {index}",
#                 category_id=category,
#                 nutriscore=index,
#                 url=f"www.test.fr {index}",
#                 ingredients="www.test.fr",
#                 photo="www.test.fr",
#                 fat_100g=0,
#                 saturate_fat_100g=0,
#                 salt_100g=0,
#                 sugars_100g=0,
#                 average_rating=0,
#             )
#         self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
#         User.objects.create_user(**self.credentials)
#         self.client.login(
#             username=self.credentials["username"], password=self.credentials["password"]
#         )
#         self.product = Product.objects.get(name="My product 1")
#         self.substitute = Product.objects.get(name="My product 2")
#         self.user = User.objects.get(username="testuser")

#     def test_rating_page(self):  # pragma: no cover

#         response = self.client.get(
#             "/rating/" + str(self.substitute.id) + "/",
#             args=(self.substitute.id,),
#             follow=True,
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_view(self):  # pragma: no cover
#         response = self.client.get(
#             reverse("substitute:rating", args=(self.substitute.id,)), follow=True,
#         )
#         self.assertEquals(response.status_code, 200)

#     def test_rating(self):  # pragma: no cover
#         response = self.client.get(
#             reverse("substitute:rating", args=(self.substitute.id,)), follow=True,
#         )
#         self.assertEquals(json.loads(response.content)["whole_avg"], 0)


class VoteTests(TestCase):
    def setUp(self):  # pragma: no cover
        Category.objects.create(name="test")
        category = Category.objects.get(name="test")
        for index in range(0, 3):
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
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.product = Product.objects.get(name="My product 1")
        self.substitute = Product.objects.get(name="My product 2")
        self.user = User.objects.get(username="testuser")

    def test_vote_page(self):  # pragma: no cover
        response = self.client.post(
            "/vote/" + str(self.substitute.id) + "/5/",
            args=(self.substitute.id, 5,),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.post(
            reverse("substitute:vote", args=(self.substitute.id, 5,)), follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_vote(self):  # pragma: no cover
        response = self.client.post(
            reverse("substitute:vote", args=(self.substitute.id, 5,)), follow=True,
        )
        self.assertEquals(json.loads(response.content)["whole_avg"], 5)
        self.assertEquals(json.loads(response.content)["number_votes"], 1)
        self.assertEquals(json.loads(response.content)["whole_avg"], 5)
        self.assertTrue(
            Rating.objects.filter(
                user_id=self.user, product_id=self.substitute, rating=5
            ).exists()
        )

    def test_unique_vote(self):  # pragma: no cover
        response = self.client.post(
            reverse("substitute:vote", args=(self.substitute.id, 5,)), follow=True,
        )
        time.sleep(10)
        response = self.client.post(
            reverse("substitute:vote", args=(self.substitute.id, 5,)), follow=True,
        )
        time.sleep(10)
        votes = Rating.objects.filter(user_id=self.user, product_id=self.substitute)
        time.sleep(3)
        self.assertTrue(len(votes) == 1)


class VoteLiveTestCase(StaticLiveServerTestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(VoteLiveTestCase, self).setUp()
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

        self.product = Product.objects.get(name="My product 1")
        self.substitute = Product.objects.get(name="My product 2")
        self.user = User.objects.get(username="usertest")
        Substitute.objects.create(
            product_id=self.product, substitute_id=self.substitute, user_id=self.user
        )
        # Login the user
        self.assertTrue(
            self.client.login(
                username=self.credentials["username"],
                password=self.credentials["password"],
            )
        )
        # Add cookie to log in the browser
        cookie = self.client.cookies["sessionid"]
        self.selenium.get(
            self.live_server_url
        )  # visit page in the site domain so the page accepts the cookie
        self.selenium.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(VoteLiveTestCase, self).tearDown()

    def test_vote(self):  # pragma: no cover
        selenium = self.selenium
        selenium.get(
            f"{self.live_server_url}/detail/{self.product.id}/{self.substitute.id}/"
        )
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        star_5 = selenium.find_element_by_class_name("star_5")
        star_5.click()

        time.sleep(3)
        classes = star_5.get_attribute("class").split(" ")
        assert "ratings_vote" in classes
        assert (
            Rating.objects.filter(
                user_id=self.user, product_id=self.substitute, rating=5
            ).exists()
            is True
        )
