# UP9 Traffic Comparison Tool

Understand regressions by comparing your API traffic snapshots. 
Before promoting release and/or merging yet another PR, review the changes in API traffic. To spot unexpected change in service communications.
Compare the traffic from automated service tests against a baseline. 
Compare against traffic from stable version or previous release.

Alternative case is front-end development, where you can spot the change in frontend communications.


As a result, the directory will be created, containing diff report. Open `index.html` in your browser to see the report.

## Alternative way
If you want to build the image yourself you can do it with:

```
docker build -t harnic .
```

Run from directory with HAR files substituting `FILE1` and `FILE2` with your file names:
```shell
docker run -it -v `pwd`:/hars harnic FILE1 FILE2
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
- Profile stats for big files
- Dynamic score ratio
- Handle soft diffs missing or added as soft (*Under question*)


**Frontend**:

- Apply prismjs to content bodies: https://betterstack.dev/blog/code-highlighting-in-react-using-prismjs/
- Add D3.js graphics
- Add collapsing of 'same' content
- Add loaders
- Add bytes limit to truncated part (*Hard*)
- Add horizontal scroll to diff (*Hard*)
- Add contextual context-wrap (*Hard*)
