Feature: Verify boAT wireless headphone is added to the cart

  Scenario: Verify user logs in and navigates to Amazon website
    Given I am on the Amazon website
    When I log in with my Amazon credentials read from excel_file
    When I should be logged in successfully
    When I click on the All icon in the middle of the web page with the search box
    When I enter product name into the search box
    When I select required brand under the Brands section on the left scroll bar tab
    Then I select the third product from the results
    Then I ensure that the same product is not already added in the cart
    Then I click on "Add to Cart"
    Then only a single product should be added to the cart
    Then I click on "Proceed to Checkout"
    And I should be taken to the checkout page for further steps in the purchase process
