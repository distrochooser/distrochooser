# Known issues

## General

## Mobile

## Desktop


### **Issues Identified:**

1. **Slider Visibility Issue**:
   - In the "Linux and You" and "Computer Knowledge" sections, the weight slider appears only next to the first question, but in other sections, the slider is displayed next to every question.
   
   **Expected Behavior**: The weight slider should appear next to all questions consistently across all sections.

2. **Non-Functional Plus/Minus Buttons**:
   - The plus (+) and minus (-) buttons next to the weight sliders do not function. Clicking them does not adjust the slider values.
   
   **Expected Behavior**: The plus/minus buttons should adjust the slider values when clicked.

3. **Improperly Formatted Results**:
   - The results at the end are not well-formatted and difficult to understand. The layout needs improvement for better clarity.

   **Expected Behavior**: The results page should be clearly formatted, making it easy to interpret the suggested distributions.

4. **Missing "Skip Question" Button**:
   - There is no "Skip Question" button, which limits user flexibility while filling out the form.
   
   **Expected Behavior**: A "Skip Question" button should be available to allow users to skip certain questions if needed.

5. **Repeated Alerts in Distribution Privacy Section**
   - Alerts for the same action appear multiple times.

6. **Some Improvements and bug fixes for setup.md**
   - To start the application there is a typo error in the command "python3 manage.py runserver".

   **Expected Behavior**: It should be "python manage.py runserver" (removed the 3)

   - Adding a command for activating application for Linux AND Windows could be helpful.

   **Expected Behavior**: Linux/MacOS: "source ./venv/bin/activate"
                          Windows: ".\venv\Scripts\activate"

---
5.2**Visual Example**:
![Issue Example](https://i.ibb.co/27BpMYm/Screenshot-2024-10-01-212641.png)


---

### **Steps to Reproduce**:
1. Navigate to the "Linux and You" and "Computer Knowledge" sections.
2. Observe that the weight slider is only displayed next to the first question.
3. Try using the plus/minus buttons to adjust the slider values.
4. Review the results page to see improper formatting.
5. Look for a "Skip Question" button, which is absent.

All these issues were according to my understanding. Please let me know if anything went wrong.
