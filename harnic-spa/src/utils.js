const truncate = (str, n) => {
    return str.length > n ? str.substr(0, n - 1) + "..." : str;
};

const calculateDiffClass = (diff, criteria, key) => {
  let keyClass = "";
  if (diff) {
    let keyDiff = diff[criteria].diff;
    if (keyDiff.removed.includes(key)) {
      keyClass = "delete";
    } else if (keyDiff.added.includes(key)) {
      keyClass = "insert";
    } else if (Object.keys(keyDiff.modified).includes(key)) {
      keyClass = "modified";
      if (keyDiff.modified[key] && keyDiff.modified[key][2] === true) {
        keyClass = "soft-modified";
      }
    }
  }
  return keyClass;
};

const getScoreLabelClass = (score) => {
  if (score < 0.25) {
    return 'negative';
  } else if (score == 1) {
    return 'positive';
  } else {
    return 'warning';
  }
};

export { truncate, calculateDiffClass, getScoreLabelClass };
 