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
  Grid,
  Modal,
  Button,
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
            {Object.entries(request.url.query_params).map(([key, values]) => {
              const diffClass = calculateDiffClass(diff, 'query_params', key);
              const diffIsNew = diffClass === 'insert' || diffClass === 'delete';
              const diffIsSoft = diffClass === 'soft-modified';
              return (
                <List.Item key={key} className={diffIsNew && diffClass}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${diffClass}`}>
                    {values.join(', ')}
                  </span>&nbsp;
                  {diffIsSoft &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }                  
                </List.Item>
              );
            })}
          </List>
        </List.Item>
        <List.Item>
          <div><b>Headers:</b></div>
          <List>
            {Object.entries(request.headers).map(([key, values]) => {
              const diffClass = calculateDiffClass(diff, 'headers', key);
              const diffIsNew = diffClass === 'insert' || diffClass === 'delete';
              const diffIsSoft = diffClass === 'soft-modified';
              return (
                <List.Item key={key} className={diffIsNew && diffClass}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${diffClass}`}>
                    {values.join(', ')}
                  </span>&nbsp;
                  {diffIsSoft &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }                  
                </List.Item>
              );
            })}
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

  const renderTextDiff = () => {
    const textDiff = diff['content'].diff.modified['text'][cmpIdx];
    if (textDiff.length < 50) {
      return(
        <List.Item key='text'>
          <div className="raw-content">
            <code>
              {textDiff.map((i,key) => (
                <div key={key} className={getDiffStringClass(i, key)}>{getDiffString(i)}</div>
              ))}
            </code>
          </div>
        </List.Item>
      );
    } else {
      return(
        <>
          <List.Item key='text'>
            <div className="raw-content">
              <code>
                {textDiff.slice(0, 25).map((i,key) => (
                  <div key={key} className={getDiffStringClass(i, key)}>{getDiffString(i)}</div>
                ))}
                <div>&nbsp;</div>
                <div>&nbsp;</div>
                <div key='truncated'>TRUNCATED...</div>
              </code>
            </div>
          </List.Item>
          <ModalScrollingContent>
            <Grid celled='internally'>
              <Grid.Row>
                <Grid.Column width={8}>
                  <Image src='https://react.semantic-ui.com/images/wireframe/image.png' />
                </Grid.Column>
                <Grid.Column width={8}>
                  <Image src='https://react.semantic-ui.com/images/wireframe/centered-paragraph.png' />
                </Grid.Column>
              </Grid.Row>
            </Grid>            
          </ModalScrollingContent>
        </>
      );      
    }
  }

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
            {Object.entries(response.headers).map(([key, values]) => {
              const diffClass = calculateDiffClass(diff, 'headers', key);
              const diffIsNew = diffClass === 'insert' || diffClass === 'delete';
              const diffIsSoft = diffClass === 'soft-modified';
              return (
                <List.Item key={key} className={diffIsNew && diffClass}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${diffClass}`}>
                    {values.join(', ')}
                  </span>&nbsp;
                  {diffIsSoft &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }
                </List.Item>
              );
            })}          
          </List>
        </List.Item>
        <List.Item>
          <div><b>Content:</b></div>
          <List>
            {Object.entries(response.content).map(([key, value]) => {
              if (key === 'text' && textModified) {
                return null;
              } else {
              const diffClass = calculateDiffClass(diff, 'content', key);
              const diffIsNew = diffClass === 'insert' || diffClass === 'delete';
              const diffIsSoft = diffClass === 'soft-modified';
              return (
                <List.Item key={key} className={diffIsNew && diffClass}>
                  <b>{key}</b>:
                  <span className={`har-data-value ${diffClass}`}>
                    {key === 'text' && value === null ? 'Content skipped' : value}
                  </span>&nbsp;
                  {diffIsSoft &&
                    <Popup
                      trigger={<Icon name='info' className='diff-label' />}
                      content='This is a soft difference. It means there is a difference beetwen values but we treat it inconsiderable'
                    />
                  }                  
                </List.Item>
              );
            }})}
            {textModified && renderTextDiff()}
          </List>
        </List.Item>
      </List>
    </pre>
  );
};

const ModalScrollingContent = ({ children }) => {
  const [open, setOpen] = React.useState(false)

  return (
    <Modal
      size='fullscreen'
      open={open}
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      trigger={<Button fluid basic color='blue'>Full diff</Button>}
    >
      <Modal.Header>/Add url1 -> urlr2 here/</Modal.Header>
      <Modal.Content scrolling>
        <Modal.Description>
          { children }
        </Modal.Description>
      </Modal.Content>
      <Modal.Actions>
        <Button onClick={() => setOpen(false)} primary>
          Proceed <Icon name='chevron right' />
        </Button>
      </Modal.Actions>
    </Modal>
  )
}


const DiffRecordRow = ({ record }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
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
        <Statistic.Value>{stats.matched}</Statistic.Value>
        <Statistic.Label>Matched</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.modified}</Statistic.Value>
        <Statistic.Label>Modified</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.added}</Statistic.Value>
        <Statistic.Label>Added</Statistic.Label>
      </Statistic>
      <Statistic>
        <Statistic.Value>{stats.removed}</Statistic.Value>
        <Statistic.Label>Removed</Statistic.Label>
      </Statistic>
    </Statistic.Group>
  </div>
)


class App extends Component {
  constructor(props) {
    super(props);

    const index = window.globalData.diff.index;
    const original_uuids = window.globalData.diff.strict_order_records;
    const reordered_uuids = window.globalData.diff.reordered_records;

    const strict_order_records = original_uuids.map(rUuid => index[rUuid]);
    const reordered_records = reordered_uuids.map(rUuid => index[rUuid]);

    const kpis = window.globalData.kpis;

    this.state = {
      filterName: null,

      strict_order_records: strict_order_records,
      reordered_records: reordered_records,

      kpis: kpis,

      showReordered: true,
    };

    if (this.state.showReordered) {
      this.state.records = reordered_records;
      this.state.stats = kpis.stats.with_reorders;
    } else {
      this.state.records = strict_order_records;
      this.state.stats = kpis.stats.strict_order;
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
      records: prevState.showReordered ? this.state.strict_order_records : this.state.reordered_records,
      stats: prevState.showReordered ? this.state.kpis.stats.strict_order : this.state.kpis.stats.with_reorders,
    }));
  }

  render() {
    let {
      kpis,
      records,
      stats,
      showReordered,
      filterName,
    } = this.state;
    if (filterName) {
      records = this.filterRecords();
    };

    const toogleProps = {};
    toogleProps['defaultChecked'] = showReordered;

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
        <Statistics stats={stats} />
        <Grid>
          <Grid.Row>
            <Grid.Column width={2} className='reorders-toogle'>
              <Checkbox toggle {...toogleProps} label='Allow reorders' onChange={this.toogleReordered}/>
              <Popup
                trigger={<Icon name='info' className='reordering-desc-icon' />}
                content='Fixes ordering of the same entries if they were mismatched due to different response time deltas.
                This is mostly caused by the nature of async requests. Those fixed entries have a special icon.'
              />
            </Grid.Column>
            <Grid.Column width={14}>
              <FilterDropdown setFilterType={this.setFilterType}/>
            </Grid.Column>
          </Grid.Row>
        </Grid>
        <Table fixed celled selectable>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>{kpis.file1.path}:&nbsp;&nbsp;{kpis.file1.num_entries} entries</Table.HeaderCell>
              <Table.HeaderCell>{kpis.file2.path}:&nbsp;&nbsp;{kpis.file2.num_entries} entries</Table.HeaderCell>
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
