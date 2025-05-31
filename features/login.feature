@ui @smoke
Feature: Login en SauceDemo
  Como usuario del sistema
  Quiero poder autenticarme con mis credenciales
  Para acceder al inventario de productos

  Background:
    Given que abro la página de login de SauceDemo

  @smoke
  Scenario: Login exitoso con credenciales válidas
    When ingreso el usuario "standard_user" y la contraseña "secret_sauce"
    And hago clic en el botón de login
    Then debería ser redirigido a la página de inventario
    And debería ver el título "Products"

  @regression
  Scenario Outline: Login fallido con credenciales inválidas
    When ingreso el usuario "<usuario>" y la contraseña "<password>"
    And hago clic en el botón de login
    Then debería ver un mensaje de error
    And debería permanecer en la página de login

    Examples:
      | usuario | password | 
      | standard_user | password_incorrecto |
      | usuario_inexistente | secret_sauce |
      | locked_out_user | secret_sauce |

  @regression
  Scenario: Login con campos vacíos
    When dejo los campos de usuario y contraseña vacíos
    And hago clic en el botón de login
    Then debería ver un mensaje de error indicando campos requeridos