# UP9 Traffic Comparison Tool

Understand regressions by comparing your API traffic snapshots. 
Before promoting release and/or merging yet another PR, review the changes in API traffic. To spot unexpected change in service communications.
Compare the traffic from automated service tests against a baseline. 
Compare against traffic from stable version or previous release.

Alternative case is front-end development, where you can spot the change in frontend communications.


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
- Handle ldjson files
- Count partial matches in match ratio
- Ignore dynamic values/IDs in HTML/XML/JSON
- Maybe some rules to ignore dynamic patterns inside body?
- Maybe ignore inner differences of error responses
- Handle url params


**Frontend**:

- Apply prismjs to content bodies: https://betterstack.dev/blog/code-highlighting-in-react-using-prismjs/
- Add D3.js graphics
- Add collapsing of 'same' content
- Add loaders


**Issues**:
- Query params compare only keys
- Add req/resp body to modal header title
- Change `...TRUNCATED..`. and `Full diff` top be more human friendly
- Add bytes limit to truncated part
- Add horizontal scroll to diff
- Add contextual context-wrap
- Rename proceed button
- Profile stats for big files
