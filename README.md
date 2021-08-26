# UP9 Traffic Comparison Tool

Make sure your image is latest:
```shell
docker pull gcr.io/mimetic-card-241611/harnic/develop
```

Run from directory with HAR files substituting `FILE1` and `FILE2` with your file names:

```shell
docker run -it -v `pwd`:/hars gcr.io/mimetic-card-241611/harnic/develop FILE1 FILE2
```

As a result, the directory will be created, containing diff report. Open `index.html` in your browser to see the report.

## Alternative way
If you want to build the image yourself you can do it with:

```
docker build -t harnic .
```

Then run with:
```
docker run -it --name harnic -v `$PWD`:/hars harnic FILE1 FILE2
docker cp harnic:/app/harnic-spa/build build
docker rm harnic
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
- if whole header is missing/added - color its name, too


**Issues**:
- Decode base64
- Diff FORMATED json
- Change seq matcher match score from 0.7 to 0.5