import React from "react";
import {
  Button,
  List,
  Grid,
  Popup,
  Icon,
  Label,
} from "semantic-ui-react";
import { DateTime } from "luxon";
import regexifyString from "regexify-string";

import ModalScrollingContent from "./ModalScrollingContent.js";
import { truncate, calculateDiffClass } from ".././utils.js";

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

const ResponseData = ({
  recordPair,
  request,
  response,
  diff,
  initialEntry,
}) => {
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

  const renderText = () => {
    const contentText = response.content["text"];
    if (!textModified) {
      if (contentText) {
        return <ContentText value={contentText} request={request} />;
      } else {
        return null;
      }
    }
    const textDiff = diff["content"].diff.modified["text"];
    if (textDiff[cmpIdx].length < 50) {
      return (
        <List.Item key="text">
          <div className="raw-content">
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

  let textModified = false;
  if (
    "text" in response.content &&
    diff &&
    "text" in diff["content"].diff.modified &&
    diff["content"].diff.modified["text"] !== null
  ) {
    textModified = true;
  }

  return (
    <pre className="har-data">
      <List>
        <List.Item>
          <div>
            <b>Recieved:</b>
            <span className="har-data-value">
              {DateTime.fromSeconds(response._ts).toISO()}
            </span>
          </div>
        </List.Item>
        <List.Item>
          <div>
            <b>Status:</b>
            <span className="har-data-value">{response.status}</span>
          </div>
        </List.Item>
        <List.Item>
          <div>
            <b>Headers:</b>
          </div>
          <List>
            {Object.entries(response.headers).map(([key, values]) => {
              const diffClass = calculateDiffClass(diff, "headers", key);
              const diffIsNew =
                diffClass === "insert" || diffClass === "delete";
              const diffIsSoft = diffClass === "soft-modified";
              return (
                <List.Item key={key} className={diffIsNew && diffClass}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${diffClass}`}>
                    {values.join(", ")}
                  </span>
                  &nbsp;
                  {diffIsSoft && (
                    <Popup
                      trigger={<Icon name="info" className="diff-label" />}
                      content="This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable"
                    />
                  )}
                </List.Item>
              );
            })}
          </List>
        </List.Item>
        <List.Item>
          <div>
            <b>Content:</b>
          </div>
          <List>
            {Object.entries(response.content).map(([key, value]) => {
              if (key === "text") {
                return null;
              } else {
                const diffClass = calculateDiffClass(diff, "content", key);
                const diffIsNew =
                  diffClass === "insert" || diffClass === "delete";
                const diffIsSoft = diffClass === "soft-modified";
                return (
                  <List.Item key={key} className={diffIsNew && diffClass}>
                    <b>{key}</b>:
                    <span className={`har-data-value ${diffClass}`}>
                      {value}
                    </span>
                    &nbsp;
                    {diffIsSoft && (
                      <Popup
                        trigger={<Icon name="info" className="diff-label" />}
                        content="This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable"
                      />
                    )}
                  </List.Item>
                );
              }
            })}
            {renderText()}
          </List>
        </List.Item>
      </List>
    </pre>
  );
};

export default ResponseData;
