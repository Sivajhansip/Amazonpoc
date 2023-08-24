Feature: Verify boAT wireless headphone is added to the cart

  @login
  Scenario: Test1: Verify user logs in and navigates to Amazon website
    Given I am on the Amazon website
    When I log in with my Amazon credentials read from excel_file
    When I should be logged in successfully

  @product-selection
  Scenario: Test2: Verify the selection of the required product
    When I click on the All icon in the middle of the web page with the search box
    When I enter "Headphones wireless" into the search box
    When I select "boAT" under the Brands section on the left scroll bar tab
    Then I select the third product from the results
    Then I ensure that the same product is not already added in the cart

  @add-to-cart
  Scenario: Test3: Verify adding the required product to the cart
    Then I click on "Add to Cart"
    Then only a single product should be added to the cart

  @proceed-to-checkout
  Scenario: Test4: Verify the "Proceed to Checkout" feature
    Then I click on "Proceed to Checkout"
    And I should be taken to the checkout page for further steps in the purchase process
