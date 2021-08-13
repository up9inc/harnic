# UP9 Traffic Comparison Tool

Run from directory with HAR files: ```docker run -it -v `pwd`:/hars gcr.io/mimetic-card-241611/harnic/develop file1.har file2.har```

### Future Ideas

---

**Backend**:
- Allow Reorder
- Count partial matches in match ratio
- Ignore dynamic values/IDs in HTML/XML/JSON
- Maybe some rules to ignore dynamic patterns inside body?
- Maybe ignore inner differences of error responses


**Frontend**:

- Apply prismjs to content bodies: https://betterstack.dev/blog/code-highlighting-in-react-using-prismjs/
- Add D3.js graphics
