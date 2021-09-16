import React from "react";
import {
  List,
  Popup,
  Icon,
} from "semantic-ui-react";
import { DateTime } from "luxon";

import HttpTxBody from "./HttpTxBody.js";
import { calculateDiffClass } from ".././utils.js";


const ResponseData = ({
  recordPair,
  request,
  response,
  diff,
  initialEntry,
  score,
}) => {
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
            <HttpTxBody
              request={request}
              response={response}
              initialEntry={initialEntry}
              diff={diff}
              recordPair={recordPair}
              score={score}
            />
          </List>
        </List.Item>
      </List>
    </pre>
  );
};

export default ResponseData;
