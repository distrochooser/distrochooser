---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ["bug"]
assignees: "cmllr"
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Please describe the bug as detailed as possible. Please also mention the expected behaviour!
      placeholder: Tell us what you see!
      value: "A bug happened!"
  - type: dropdown
    id: mobile
    attributes:
      label: Version
      description: Is the device a mobile device?
      options:
        - Yes
        - No
    
  - type: dropdown
    id: instance
    attributes:
      label: What page were you using?
      multiple: false
      options:
        - distrochooser.de
        - beta.distrochooser.de