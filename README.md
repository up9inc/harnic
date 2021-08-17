# UP9 Traffic Comparison Tool

Run from directory with HAR files substituting `FILE1` and `FILE2` with your file names:

```
docker run -it --name harnic -v `$PWD`:/hars harnic FILE1 FILE2
docker cp harnic:/app/harnic-spa/build build
docker rm harnic
```

If you want to build the image yourself you can do it with:

```
docker build -t harnic .
```

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
