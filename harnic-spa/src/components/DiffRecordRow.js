import { useState } from "react";
import { Tab, Table, Icon, Label } from "semantic-ui-react";

import RequestData from "./RequestData.js";
import ResponseData from "./ResponseData.js";
import { truncate } from ".././utils.js";

const DiffRecordRow = ({ record }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const handleToggle = () => setIsOpen(!isOpen);
  const handleTabChange = (e, { activeIndex }) => setActiveIndex(activeIndex);

  const toggleStyle = {
    display: isOpen ? "table-row" : "none",
  };

  const rowClassMap = {
    delete: "negative",
    insert: "positive",
    diff: "warning",
    equal: "normal",
  };
  const reqMethodClassMap = {
    get: "blue",
    post: "green",
    delete: "red",
    patch: "orange",
  };

  const aPanes = record.pair.a
    ? [
        {
          menuItem: "Request",
          render: () => (
            <Tab.Pane>
              <RequestData
                request={record.pair.a.request}
                diff={record.diff && record.diff.comparisons.request}
              />
            </Tab.Pane>
          ),
        },
        {
          menuItem: "Response",
          render: () => (
            <Tab.Pane>
              <ResponseData
                recordPair={record.pair}
                request={record.pair.a.request}
                response={record.pair.a.response}
                diff={record.diff && record.diff.comparisons.response}
                initialEntry={true}
              />
            </Tab.Pane>
          ),
        },
      ]
    : [];

  const ADiffTab = () => (
    <Tab
      panes={aPanes}
      activeIndex={activeIndex}
      onTabChange={handleTabChange}
    />
  );

  const bPanes = record.pair.b
    ? [
        {
          menuItem: "Request",
          render: () => (
            <Tab.Pane>
              <RequestData
                request={record.pair.b.request}
                diff={record.diff && record.diff.comparisons.request}
              />
            </Tab.Pane>
          ),
        },
        {
          menuItem: "Response",
          render: () => (
            <Tab.Pane>
              <ResponseData
                recordPair={record.pair}
                request={record.pair.b.request}
                response={record.pair.b.response}
                diff={record.diff && record.diff.comparisons.response}
                initialEntry={false}
              />
            </Tab.Pane>
          ),
        },
      ]
    : [];

  const BDiffTab = () => (
    <Tab
      panes={bPanes}
      activeIndex={activeIndex}
      onTabChange={handleTabChange}
    />
  );

  return (
    <>
      <Table.Row className={rowClassMap[record.tag]} onClick={handleToggle}>
        <Table.Cell>
          {record.pair.a && (
            <>
              <Label
                size="mini"
                color={
                  reqMethodClassMap[record.pair.a.request.method.toLowerCase()]
                }
                basic
              >
                {record.pair.a.request.method}
              </Label>
              &nbsp;&nbsp;
              {truncate(record.pair.a.request.url.url, 150)}
            </>
          )}
          {record.is_reordering && (
            <Icon name="exchange" className="reordering-icon" />
          )}
        </Table.Cell>
        <Table.Cell>
          {record.pair.b && (
            <>
              <Label
                size="mini"
                color={
                  reqMethodClassMap[record.pair.b.request.method.toLowerCase()]
                }
                basic
              >
                {record.pair.b.request.method}
              </Label>
              &nbsp;&nbsp;
              {truncate(record.pair.b.request.url.url, 150)}
            </>
          )}
        </Table.Cell>
      </Table.Row>

      <Table.Row style={toggleStyle}>
        <Table.Cell colSpan={1} className="entry-data">
          {record.pair.a && isOpen && <ADiffTab />}
        </Table.Cell>
        <Table.Cell colSpan={1} className="entry-data">
          {record.pair.b && isOpen && <BDiffTab />}
        </Table.Cell>
      </Table.Row>
    </>
  );
};

export default DiffRecordRow;
