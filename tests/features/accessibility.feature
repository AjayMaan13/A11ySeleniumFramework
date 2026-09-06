Feature: Automated accessibility scanning

  Scenario: Detect missing alt text
    Given a page with missing alt text
    When the accessibility scanner runs
    Then a WCAG 1.1.1 violation is reported

  Scenario: Detect insufficient color contrast
    Given a page with insufficient color contrast
    When the accessibility scanner runs
    Then a WCAG 1.4.3 violation is reported

  Scenario: Detect unlabeled form fields
    Given a page with unlabeled form fields
    When the accessibility scanner runs
    Then a WCAG 3.3.2 violation is reported
