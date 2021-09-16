import {
  List,
  Popup,
  Icon,
} from "semantic-ui-react";
import { DateTime } from "luxon";

import HttpTxBody from "./HttpTxBody.js";
import { calculateDiffClass } from ".././utils.js";


const RequestData = ({
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
            <b>Started:</b>
            <span className="har-data-value">
              {DateTime.fromSeconds(request._ts).toISO()}
            </span>
          </div>
        </List.Item>
        <List.Item>
          <div>
            <b>Method:</b>
            <span className="har-data-value">{request.method}</span>
          </div>
        </List.Item>
        <List.Item>
          <div>
            <b>Body size:</b>
            <span className="har-data-value">{request.bodySize}</span>
          </div>
        </List.Item>
        <List.Item>
          <div>
            <b>Query params:</b>
          </div>
          <List>
            {Object.entries(request.url.query_params).map(([key, values]) => {
              const diffClass = calculateDiffClass(diff, "query_params", key);
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
            <b>Headers:</b>
          </div>
          <List>
            {Object.entries(request.headers).map(([key, values]) => {
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
        {request.post_data &&
          <List.Item>
            <div>
              <b>Post Data:</b>         
            </div>
            <List>
              {Object.entries(request.post_data).map(([key, value]) => {
                if (key === "text") {
                  return null;
                } else {
                  const diffClass = calculateDiffClass(diff, "postData", key);
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
                parent='request'
                request={request}
                response={response}
                initialEntry={initialEntry}
                diff={diff}
                recordPair={recordPair}
                score={score}
              />
            </List>
          </List.Item>
        }
      </List>
    </pre>
  );
};

export default RequestData;