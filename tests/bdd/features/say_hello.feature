Feature: Say hello
  As a user
  I want to greet someone
  So that I see a friendly message

  Scenario: Greet a person by name
    When I run "hello-world hello say Alice"
    Then the output contains "Hello, Alice!"

