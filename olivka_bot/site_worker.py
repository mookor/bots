from typing import List
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import datetime
from bd import DataBase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserWorker:
    def __init__(self) -> None:
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        week_day = datetime.datetime.today().weekday()
        current_hour = datetime.datetime.today().hour
        self.browser = webdriver.Chrome(chrome_options=options)
        week_day +=1
        if week_day>7:
            week_day = 1
        if current_hour > 12:
            self.browser.get(f'https://corp.olivkafood.ru/?day_of_week={week_day+1}')
        else:
            self.browser.get(f'https://corp.olivkafood.ru/?day_of_week={week_day}')
        

    def move_and_click(self, field: str) -> None:
        ActionChains(self.browser).move_to_element(field).perform()
        ActionChains(self.browser).click(field).perform()

    def set_users(self, users: List[str]) -> None:
        self.number_of_persons = len(users)
        if self.number_of_persons > 5:
            add_button = self.browser.find_element_by_class_name("corp-add-person")
            for i in range(self.number_of_persons - 5):
                add_button.click()

        persons = self.browser.find_elements_by_class_name("corp-person-head")
        for i, person in enumerate(persons[: self.number_of_persons]):
            self.move_and_click(person)
            person_info = person.find_element_by_class_name("person-info")
            person_name_input = person_info.find_element_by_class_name("form-control")
            person_name_input.send_keys(users[i])

    def set_products(self, products: List[str], person_number: int) -> None:
        all_table = self.browser.find_element_by_class_name("corp-table")
        categories = all_table.find_elements_by_class_name("corp-category")
        products = [p.lower() for p in products]
        products = [p if p != "????????????" else "???????? ???? 16.00" for p in products]
        for cat in categories:
            items = cat.find_elements_by_class_name("corp-item-wrap")
            for item in items:
                if len(products) == 0:
                    break
                item_selector = item.find_element_by_css_selector(".corp-item")
                item_name = item_selector.text.split("\n")[0]

                if item_name.lower() in products:
                    person_product_selector = (
                        item_selector.find_element_by_css_selector(
                            f".corp-person.pers_{person_number+1}"
                        )
                    )
                    person_input_form = (
                        person_product_selector.find_element_by_class_name(
                            "form-control"
                        )
                    )
                    person_input_form.send_keys("1")
                    products.remove(item_name.lower())
        return products

    def get_default(self):
        all_table = self.browser.find_element_by_class_name("corp-table")
        categories = all_table.find_elements_by_class_name("corp-category")
        default_cat = categories[0].find_elements_by_class_name("corp-item-wrap")[1]
        items = default_cat.text.split("\n")[2]
        items = items.replace(", ","\n")
        return items

    def set_final_fields(self, name, phone, email):
        order_form = self.browser.find_element_by_class_name("basket-form")
        name_phone_instruments = order_form.find_elements_by_class_name("col-xs-6")

        duty_name = name_phone_instruments[0].find_element_by_class_name("form-control")
        duty_name.send_keys(name)

        phone_form = name_phone_instruments[1].find_element_by_class_name(
            "form-control"
        )
        phone_form.send_keys(phone)

        instruments_form = name_phone_instruments[4].find_element_by_class_name(
            "form-control"
        )
        instruments_form.send_keys(Keys.BACKSPACE)
        instruments_form.send_keys(str(self.number_of_persons))

        email_payment_delivery = order_form.find_elements_by_class_name("col-xs-12")
        email_form = email_payment_delivery[0].find_element_by_class_name(
            "form-control"
        )
        email_form.send_keys(email)

        payment_select = Select(
            email_payment_delivery[1].find_element_by_class_name("form-control")
        )
        payment_select.select_by_visible_text("???????????? ???????????????????? ???????????? ??????????????")

        delivery_select = Select(
            email_payment_delivery[2].find_element_by_class_name("form-control")
        )
        delivery_select.select_by_visible_text("????????????")

        region_select = Select(
            order_form.find_element_by_id("order_district").find_element_by_class_name(
                "form-control"
            )
        )
        region_select.select_by_value("6")

        addres = email_payment_delivery[3].find_elements_by_class_name("form-control")
        addres[0].send_keys("??????????????????????????")
        addres[1].send_keys("18/1")
        addres[2].send_keys("246")
        btn = order_form.find_element_by_name("yt0")
        self.move_and_click(btn)


# all_table = browser.find_element_by_class_name("corp-table")
# categories = all_table.find_elements_by_class_name("corp-category")
# for cat in categories:
#     items = cat.find_elements_by_class_name("corp-item-wrap")
#     for item in items:
#         item_name = item.find_element_by_css_selector(".corp-item").text.split("\n")[0]
# bw = BrowserWorker()
# bw.set_users(["??????????","????????????","????????????","????????????","????????????","????????????","????????????"])
# # bw.set_products(["?????????? ???????????????? 130 ????", "???????? ???? ???????????????? 400/20 ????"],0)
# # bw.set_products(["???????? ?? ??????????, ?????????????? ?? ?????????????? ??????????????", "???????????????? ????????????????????????   130/50????"],1)
# # bw.set_products(["???????? ?? ?????????????????? ???????????????????? ?? ??????????????", "?????????? ???????????????? 130 ????", "???????????? ???????????????? 330 ????"],2)
# bw.set_final_fields("????????????", "9930165002", "123")
