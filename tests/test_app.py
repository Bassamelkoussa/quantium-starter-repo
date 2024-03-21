# tests/test_app.py

import pytest
from selenium.webdriver.common.by import By
from dash.testing.application_runners import import_app


def test_header_is_present(dash_duo):
    app = import_app("my_dash_app.app")  # Replace with the actual path to your Dash app
    dash_duo.start_server(app)

    # Check if the header is present
    assert dash_duo.find_element("h1").text == "Sales, Price, and Quantity Data Over Time"


def test_visualisation_is_present(dash_duo):
    app = import_app("my_dash_app.app")  # Replace with the actual path to your Dash app
    dash_duo.start_server(app)

    # Check if the visualisation is present
    assert dash_duo.find_element("#sales-price-graph")
    assert dash_duo.find_element("#sales-quantity-graph")


def test_region_picker_is_present(dash_duo):
    app = import_app("my_dash_app.app")  # Replace with the actual path to your Dash app
    dash_duo.start_server(app)

    # Check if the region picker is present
    radio_items = dash_duo.find_element("#region-radio")
    options = radio_items.find_elements(By.CSS_SELECTOR, "input[type=radio]")
    assert len(options) > 0, "No radio items found for region picker"
