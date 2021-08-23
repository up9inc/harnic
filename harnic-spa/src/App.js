import React, {
  Component,
  Fragment,
  useState
} from 'react';
import 'semantic-ui-css/semantic.min.css';
import {
  Container,
  Header,
  Table,
  Label,
  Tab,
  List,
  Dropdown,
  Image,
  Icon,
  Statistic,
  Popup,
  Checkbox,
  Segment,
  Grid
} from 'semantic-ui-react';
import {
  DateTime
} from "luxon";
import regexifyString from "regexify-string";
import _ from 'lodash';


import logo from './logo.svg';
import './App.css';
import {
  truncate,
  fetchLocal,
} from './utils.js';


const calculateDiffClass = (diff, criteria, key) => {
  let keyClass = '';
  if (diff) {
    let keyDiff = diff[criteria].diff;
    if (keyDiff.removed.includes(key)) {
      keyClass = 'delete';
    } else if (keyDiff.added.includes(key)) {
      keyClass = 'insert';
    } else if (Object.keys(keyDiff.modified).includes(key)) {
      keyClass = 'modified';
      if (keyDiff.modified[key] && (keyDiff.modified[key][2] === true)) {
        keyClass = 'soft-modified';
      };
    };
  };
  return keyClass;
};


const RequestData = ({ request, diff }) => {
  return (
    <pre className="har-data">
      <List>
        <List.Item>
          <div><b>Started:</b><span className="har-data-value">{DateTime.fromSeconds(request._ts).toISO()}</span></div>
        </List.Item>
        <List.Item>
          <div><b>Method:</b><span className="har-data-value">{request.method}</span></div>
        </List.Item>
        <List.Item>
          <div><b>Body size:</b><span className="har-data-value">{request.bodySize}</span></div>
        </List.Item>
        <List.Item>
          <div><b>Query params:</b></div>
          <List>
            {Object.entries(request.url.query_params).map(([key, values]) =>
                <List.Item key={key}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${calculateDiffClass(diff, 'query_params', key)}`}>{values.join(', ')}</span>
                </List.Item>
            )}
          </List>
        </List.Item>
        <List.Item>
          <div><b>Headers:</b></div>
          <List>
            {Object.entries(request.headers).map(([key, values]) => 
                <List.Item key={key}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${calculateDiffClass(diff, 'headers', key)}`}>
                    {values.join(', ')}
                  </span>&nbsp;
                  {calculateDiffClass(diff, 'headers', key) == 'soft-modified' &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }                  
                </List.Item>
            )}
          </List>
        </List.Item>
      </List>
    </pre>
  );
};


const ResponseData = ({ response, diff, initialEntry }) => {
  const cmpIdx = initialEntry ? 0 : 1;

  const getDiffStringClass = (string, key) => {
    let cls = '';
    if (diff['content'].diff.modified['text'][2][key]){
      if (cmpIdx === 0) {
        cls = 'content-diff-removed'; 
      } else {
        cls = 'content-diff-added'; 
      }
    }
    return cls;
  };

  const getDiffString = string => {
    const wholeLineRegex = /^\u0000[\+\^-](.+?)\u0001$/g;
    const regex = /\u0000[\+\^-](.+?)\u0001/g;
    if (string.match(wholeLineRegex)) {
      return <>{' ' + string.slice(2)}</>;
    }
    string = regexifyString({
        pattern: regex,
        decorator: (match, index) => {
          const cls = initialEntry ? "inner-line-diff removed" : "inner-line-diff added";
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

  const renderTextDiff = () => (
    <div className="raw-content">
      <code>
        {diff['content'].diff.modified['text'][cmpIdx].map((i,key) => (
          <div key={key} className={getDiffStringClass(i, key)}>{getDiffString(i)}</div>
        ))}
      </code>
    </div>
  )

  let textModified = false;
  if ('text' in response.content &&
      diff &&
      'text' in diff['content'].diff.modified &&
      diff['content'].diff.modified['text'] !== null) {
    textModified = true;
  }

  return (
    <pre className="har-data">
      <List>
        <List.Item>
          <div><b>Recieved:</b><span className="har-data-value">{DateTime.fromSeconds(response._ts).toISO()}</span></div>
        </List.Item>
        <List.Item>
          <div><b>Status:</b><span className="har-data-value">{response.status}</span></div>
        </List.Item>
        <List.Item>
          <div><b>Headers:</b></div>
          <List>
            {Object.entries(response.headers).map(([key, values]) => 
                <List.Item key={key}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${calculateDiffClass(diff, 'headers', key)}`}>
                    {values.join(', ')}
                  </span>&nbsp;
                  {calculateDiffClass(diff, 'headers', key) == 'soft-modified' &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }
                </List.Item>
            )}          
          </List>
        </List.Item>
        <List.Item>
          <div><b>Content:</b></div>
          <List>
            {Object.entries(response.content).map(([key, value]) => (
                key === 'text' && textModified ? null :
                <List.Item key={key}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${calculateDiffClass(diff, 'content', key)}`}>
                    {key === 'text' && value === null ? 'Raw data too big' : value}
                  </span>
                </List.Item>
            ))}
            {textModified &&
              <List.Item key='text'>
                {renderTextDiff()}
              </List.Item>
            }
          </List>
        </List.Item>
      </List>
    </pre>
  );
};


const DiffRecordRow = ({ record }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(1);
  const handleToggle = () => setIsOpen(!isOpen);
  const handleTabChange = (e, { activeIndex }) => setActiveIndex(activeIndex);

  const toggleStyle = {
    display: isOpen ? "table-row" : "none"
  };

  const rowClassMap = {'delete': 'negative', 'insert': 'positive', 'diff': 'warning', 'equal': 'normal'};
  const reqMethodClassMap = {'get': 'blue', 'post': 'green', 'delete': 'red', 'patch': 'orange'};

  const aPanes = record.pair.a ? [
    { menuItem: 'Request', render: () => (
      <Tab.Pane>
        <RequestData
          request={record.pair.a.request}
          diff={record.diff && record.diff.comparisons.request}
        />
      </Tab.Pane>
    )},
    { menuItem: 'Response', render: () => (
      <Tab.Pane>
        <ResponseData
          response={record.pair.a.response}
          diff={record.diff && record.diff.comparisons.response}
          initialEntry={true}
        />      
      </Tab.Pane>
    )},
  ] : [];

  const ADiffTab = () => <Tab panes={aPanes} activeIndex={activeIndex} onTabChange={handleTabChange} />;

  const bPanes = record.pair.b ? [
    { menuItem: 'Request', render: () => (
      <Tab.Pane>
        <RequestData
          request={record.pair.b.request}
          diff={record.diff && record.diff.comparisons.request}
        />
      </Tab.Pane>
    )},
    { menuItem: 'Response', render: () => (
      <Tab.Pane>
        <ResponseData
          response={record.pair.b.response}
          diff={record.diff && record.diff.comparisons.response}
          initialEntry={false}
        />      
      </Tab.Pane>
    )},
  ] : [];

  const BDiffTab = () => <Tab panes={bPanes} activeIndex={activeIndex} onTabChange={handleTabChange} />;

  return (
    <>
      <Table.Row className={rowClassMap[record.tag]} onClick={handleToggle}>
        <Table.Cell>
          {record.pair.a && 
            <>
              <Label
                size='mini'
                color={reqMethodClassMap[record.pair.a.request.method.toLowerCase()]}
                basic
              >
                {record.pair.a.request.method}
              </Label>&nbsp;&nbsp;
              {truncate(record.pair.a.request.url.url, 150)}
            </>
          }
          {record.is_reordering && <Icon name='exchange' className='reordering-icon' />}
        </Table.Cell>
        <Table.Cell>
          {record.pair.b && 
            <>
              <Label
                size='mini'
                color={reqMethodClassMap[record.pair.b.request.method.toLowerCase()]}
                basic
              >
                {record.pair.b.request.method}
              </Label>&nbsp;&nbsp;
              {truncate(record.pair.b.request.url.url, 150)}
            </>
          }
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


const FilterDropdown = ({setFilterType}) => {
  const options = [
    {
      key: 1,
      text: 'All',
      value: 1,
      content: (
        <Header icon='table' content='All' subheader='Shows all compared hars records' onClick={() => setFilterType('')}/>
      ),
    },
    {
      key: 2,
      text: 'Changes',
      value: 2,
      content: (
        <Header
          icon='list'
          content='Changes'
          subheader='Shows all records except those that are equal'
          onClick={() => setFilterType('diff')}          
        />
      ),
    },  
    {
      key: 3,
      text: 'Modified entries',
      value: 3,
      content: (
        <Header
          icon='exchange'
          content='Modifed'
          subheader='Shows only modified records'
          onClick={() => setFilterType('modified')}
        />
      ),
    },  
    {
      key: 4,
      text: 'Added',
      value: 4,
      content: (
        <Header
          icon='plus'
          content='Added'
          subheader='Shows all added records from second har'
          onClick={() => setFilterType('added')}
        />
      ),
    },
    {
      key: 5,
      text: 'Removed',
      value: 5,
      content: (
        <Header
          icon='minus'
          content='Removed'
          subheader='Shows all removed records from second har'
          onClick={() => setFilterType('removed')}          
        />
      ),
    },  
  ];
  return <Dropdown selection fluid floating options={options} placeholder='Filter' />;
}


const Statistics = ({stats}) => (
  <div className="statistics">
    <Statistic.Group widths='5'>
      <Statistic>
        <Statistic.Value>{(stats.ratio*100).toFixed(1)}%</Statistic.Value>
        <Statistic.Label>Match ratio</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.equal}</Statistic.Value>
        <Statistic.Label>Matched</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.diff}</Statistic.Value>
        <Statistic.Label>Diffs</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.insert}</Statistic.Value>
        <Statistic.Label>Added</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.delete}</Statistic.Value>
        <Statistic.Label>Removed</Statistic.Label>
      </Statistic>
    </Statistic.Group>
  </div>
)


class App extends Component {
  constructor(props) {
    super(props);

    const index = window.globalData.diff.index;
    const original_uuids = window.globalData.diff.original_records;
    const reordered_uuids = window.globalData.diff.reordered_records;

    let original_records = original_uuids.map(rUuid => index[rUuid]);
    let reordered_records = reordered_uuids.map(rUuid => index[rUuid]);

    let original_stats = window.globalData.stats.original;
    let reordered_stats = window.globalData.stats.with_reorders;

    this.state = {
      filterName: null,
      hars: window.globalData.hars,

      original_records: original_records,
      reordered_records: reordered_records,
      records: original_records,

      original_stats: original_stats,
      reordered_stats: reordered_stats,
      stats: original_stats,

      showReordered: false,
    };
  };

  setFilterType = (filterName) => {
    this.setState({filterName: filterName});
  };

  filterRecords = () => {
    const filter = this.state.filterName;
    let records = this.state.records.slice();
    if (filter === 'added') {
      records = records.filter(record => record.pair.a == null)
    } else if (filter === 'removed') {
      records = records.filter(record => record.pair.b == null)
    } else if (filter === 'modified') {
      records = records.filter(record => record.diff && !record.diff.equal)
    } else if (filter === 'diff') {
      records = records.filter(record => !record.diff || (record.diff && !record.diff.equal))
    };
    return records;
  }

  toogleReordered = () => {
    this.setState(prevState => ({
      showReordered: !prevState.showReordered,
      records: prevState.showReordered ? this.state.original_records : this.state.reordered_records,
      stats: prevState.showReordered ? this.state.original_stats : this.state.reordered_stats,
    }));
  }

  render() {
    let {
      hars,
      records,
      stats,
      filterName,
      showReordered,
    } = this.state;
    if (filterName) {
      records = this.filterRecords();
    };

    return (
      <Container>
        <Container className="header-container">
          <div className="item">
            <Image src={logo} size='small' wrapped />
          </div>
          <div className="item header page-header">
            <Header size='huge'>Traffic comparison tool</Header>
          </div>
        </Container>
        {Object.keys(stats).length !== 0 && <Statistics stats={stats} />}
        <Grid>
          <Grid.Row>
            <Grid.Column width={2} className='reorders-toogle'>
              <Checkbox toggle label='Allow reorders' onChange={this.toogleReordered}/>
            </Grid.Column>
            <Grid.Column width={14}>
              <FilterDropdown setFilterType={this.setFilterType}/>
            </Grid.Column>
          </Grid.Row>
        </Grid>
        <Table fixed celled selectable>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>{hars[0]}:&nbsp;&nbsp;{stats.from_count} entries</Table.HeaderCell>
              <Table.HeaderCell>{hars[1]}:&nbsp;&nbsp;{stats.to_count} entries</Table.HeaderCell>
            </Table.Row>
          </Table.Header>

          <Table.Body>
            {records.map(record => (
              <DiffRecordRow
                key={record.id}
                record={record}
              />
            ))}
          </Table.Body>      
        </Table>
      </Container>
    );
  }
}

export default App;
