import {
  Button,
  List,
  Grid,
  Popup,
  Icon,
  Label,
} from "semantic-ui-react";
import regexifyString from "regexify-string";

import ModalScrollingContent from "./ModalScrollingContent.js";
import { truncate, calculateDiffClass, getScoreLabelClass, decimalAdjust } from ".././utils.js";

const ContentText = ({ value, request }) => {
  if (value === null) {
    return "Content skipped";
  }
  let lines = value.split(/\n/);
  if (lines.length < 50) {
    return (
      <div className="raw-content">
        <code>
          {lines.map((i, key) => (
            <div key={key}>{i}</div>
          ))}
        </code>
      </div>
    );
  } else {
    const header = request.url.url;
    const trigger = (
      <Button fluid basic color="grey">
        Open full body
      </Button>
    );
    return (
      <>
        <div className="raw-content">
          <code>
            {lines.slice(0, 15).map((i, key) => (
              <div key={key}>{i}</div>
            ))}
            <div>&nbsp;</div>
            <div>&nbsp;</div>
            <div key="truncated" className="truncated grey">
              Full body is too long to be displayed here...
            </div>
          </code>
        </div>
        <ModalScrollingContent header={header} trigger={trigger}>
          <div className="raw-content">
            <code>
              {lines.map((i, key) => (
                <div key={key}>{i}</div>
              ))}
            </code>
          </div>
        </ModalScrollingContent>
      </>
    );
  }
};


const HttpTxBody = ({initialEntry, diff, request, response, recordPair, score}) => {
  const cmpIdx = initialEntry ? 0 : 1;

  const getDiffStringClass = (string, key, diffCmpIdx = cmpIdx) => {
    let cls = "";
    if (diff["content"].diff.modified["text"][2][key]) {
      cls = diffCmpIdx ? "content-diff-added" : "content-diff-removed";
    }
    return cls;
  };

  const getDiffString = (string, diffCmpIdx = cmpIdx) => {
    const wholeLineRegex = /^\u0000[\+\^-](.+?)\u0001$/g;
    const regex = /\u0000[\+\^-](.+?)\u0001/g;
    if (string.match(wholeLineRegex)) {
      return <>{" " + string.slice(2)}</>;
    }
    string = regexifyString({
      pattern: regex,
      decorator: (match, index) => {
        const cls = diffCmpIdx
          ? "inner-line-diff added"
          : "inner-line-diff removed";
        return (
          <span className={cls}>
            {/*excludes wrappers ^\0(+|-|^){} to {}\1 */}
            {match.slice(2, -1)}
          </span>
        );
      },
      input: string,
    });

    return string;
  };

  let textModified = false;
  if (
    "text" in response.content &&
    diff &&
    "text" in diff["content"].diff.modified &&
    diff["content"].diff.modified["text"] !== null
  ) {
    textModified = true;
  }

  const renderText = (parent) => {
    let txObj, txKey, txScore;
    if (parent === 'request') {
      txObj = request;
      txKey = 'postData';
      txScore = score && score.full.request;
    } else {
      txObj = response;
      txKey = 'content';
      txScore = score && score.full.response;
    }
    const contentText = txObj.content["text"];
    if (!textModified) {
      if (contentText) {
        return <ContentText value={contentText} request={request} />;
      } else {
        return null;
      }
    }
    const textDiff = diff[txKey].diff.modified["text"];
    if (textDiff[cmpIdx].length < 50) {
      return (
        <List.Item key="text">
          <div className="raw-content">
            {score && 
                <Label className={'content-score-label ' + getScoreLabelClass(txScore.content)}>
                  {decimalAdjust('floor', txScore.content * 100, -1)}%
                </Label>
            }
            <code>
              {textDiff[cmpIdx].map((i, key) => (
                <div key={key} className={getDiffStringClass(i, key)}>
                  {getDiffString(i)}
                </div>
              ))}
            </code>
          </div>
        </List.Item>
      );
    } else {
      const header = (
        <Grid celled="internally">
          <Grid.Row>
            <Grid.Column width={8}>
              <Label basic horizontal size='large'>
                Response
              </Label>
              <span className='diff-modal-header-lablel'>
                {truncate(recordPair.a.request.url.url, 75)}
              </span>
            </Grid.Column>
            <Grid.Column width={8}>
              <Label basic horizontal size='large'>
                Response
              </Label>
              {truncate(recordPair.b.request.url.url, 75)}
            </Grid.Column>
          </Grid.Row>
        </Grid>
      );
      const trigger = (
        <Button fluid basic color="orange">
          Open full difference
        </Button>
      );
      return (
        <>
          <List.Item key="text">
            <div className="raw-content">
              {score && 
                  <Label className={'content-score-label ' + getScoreLabelClass(txScore.content)}>
                    {decimalAdjust('floor', txScore.content * 100, -1)}%
                  </Label>
              }
              <code>
                {textDiff[cmpIdx].slice(0, 15).map((i, key) => (
                  <div key={key} className={getDiffStringClass(i, key)}>
                    {getDiffString(i)}
                  </div>
                ))}
                <div>&nbsp;</div>
                <div>&nbsp;</div>
                <div key="truncated" className="truncated orange">
                  Full body is too long to be displayed here...
                </div>
              </code>
            </div>
          </List.Item>
          <ModalScrollingContent header={header} trigger={trigger}>
            <Grid celled="internally">
              <Grid.Row>
                <Grid.Column width={8}>
                  <List.Item key="text">
                    <div className="raw-content">
                      <code>
                        {textDiff[0].map((i, key) => (
                          <div
                            key={key}
                            className={getDiffStringClass(i, key, 0)}
                          >
                            {getDiffString(i, 0)}
                          </div>
                        ))}
                      </code>
                    </div>
                  </List.Item>
                </Grid.Column>
                <Grid.Column width={8}>
                  <List.Item key="text">
                    <div className="raw-content">
                      <code>
                        {textDiff[1].map((i, key) => (
                          <div
                            key={key}
                            className={getDiffStringClass(i, key, 1)}
                          >
                            {getDiffString(i, 1)}
                          </div>
                        ))}
                      </code>
                    </div>
                  </List.Item>
                </Grid.Column>
              </Grid.Row>
            </Grid>
          </ModalScrollingContent>
        </>
      );
    }
  };

  return renderText('response');
};


export default HttpTxBody;