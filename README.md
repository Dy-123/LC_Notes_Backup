### Export Leetcode Notes To HTML
Setup:
*  Install python, pip and chrome/chromeDriver
*  pip install selenium
*  pip install beautifulsoup4
*  Open browser login and go to console -> application -> cookies and copy LEETCODE_SESSION value. In Python, assign this value to SESSION_COOKIE_VALUE .
*  For slow internet adjust the 'waitAfterRefreshTime' variable as needed

To run:  
```python exportLeetcodeNotesToHtml.py <url>```
