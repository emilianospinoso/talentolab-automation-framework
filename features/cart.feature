@ui @regression
Feature: Carrito de compras
  Como usuario autenticado
  Quiero poder agregar productos al carrito
  Para luego proceder con la compra

  Background:
    Given que estoy logueado en SauceDemo con usuario "standard_user"
    And estoy en la página de inventario

  @smoke
  Scenario: Agregar un producto al carrito
    Given que el carrito está vacío
    When agrego el producto "Sauce Labs Backpack" al carrito
    Then el contador del carrito debería mostrar "1"
    And el botón del producto debería cambiar a "Remove"

  @regression
  Scenario: Agregar múltiples productos al carrito
    Given que el carrito está vacío
    When agrego los siguientes productos al carrito:
      | Sauce Labs Backpack |
      | Sauce Labs Bike Light |
      | Sauce Labs Bolt T-Shirt |
    Then el contador del carrito debería mostrar "3"

  Scenario: Verificar que el carrito mantiene productos entre páginas
    Given que he agregado "Sauce Labs Backpack" al carrito
    When navego a otra sección y vuelvo al inventario
    Then el contador del carrito debería seguir mostrando "1"