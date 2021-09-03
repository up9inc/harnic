import {
  List,
  Popup,
  Icon,
} from "semantic-ui-react";
import { DateTime } from "luxon";

import { calculateDiffClass } from ".././utils.js";


const RequestData = ({ request, diff }) => {
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
      </List>
    </pre>
  );
};

export default RequestData;