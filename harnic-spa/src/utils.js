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

const decimalAdjust = (type, value, exp) => {
  // If the exp is undefined or zero...
  if (typeof exp === 'undefined' || +exp === 0) {
    return Math[type](value);
  }
  value = +value;
  exp = +exp;
  // If the value is not a number or the exp is not an integer...
  if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
    return NaN;
  }
  // Shift
  value = value.toString().split('e');
  value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
  // Shift back
  value = value.toString().split('e');
  return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
}

export { truncate, calculateDiffClass, getScoreLabelClass, decimalAdjust };
 