import React, { Component, Fragment, useState } from 'react'
import 'semantic-ui-css/semantic.min.css'
import {
  Container,
  Header,
  Table,
  Label,
  Tab,
  List,
  Dropdown,
} from 'semantic-ui-react'

import logo from './logo.svg';
import './App.css';
import {
  truncate,
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
    };
  };
  return keyClass;
};


const RequestData = ({ request, diff }) => {
  return (
    <List>
      <List.Item>
        <div><b>Started:</b> {request._ts}</div>
      </List.Item>
      <List.Item>
        <div><b>Method:</b> {request.method}</div>
      </List.Item>
      <List.Item>
        <div><b>Body size:</b> {request.bodySize}</div>
      </List.Item>
      <List.Item>
        <div><b>Query params:</b></div>
        <List>
          {Object.entries(request.url.query_params).map(([key, values]) =>
              <List.Item key={key}>
                <b>{key}</b>:&nbsp;
                <span className={calculateDiffClass(diff, 'query_params', key)}>{values.join(', ')}</span>
              </List.Item>
          )}
        </List>
      </List.Item>
      <List.Item>
        <div><b>Headers:</b></div>
        <List>
          {Object.entries(request.headers).map(([key, values]) => 
              <List.Item key={key}>
                <b>{key}</b>:&nbsp;
                <span className={calculateDiffClass(diff, 'headers', key)}>{values.join(', ')}</span>
              </List.Item>
          )}
        </List>
      </List.Item>
    </List>
  );
};


const ResponseData = ({ response, diff }) => {
  return (
    <List>
      <List.Item>
        <div><b>Recieved:</b> {response._ts}</div>
      </List.Item>
      <List.Item>
        <div><b>Status:</b> {response.status}</div>
      </List.Item>
      <List.Item>
        <div><b>Headers:</b></div>
        <List>
          {Object.entries(response.headers).map(([key, values]) => 
              <List.Item key={key}>
                <b>{key}</b>:&nbsp;
                <span className={calculateDiffClass(diff, 'headers', key)}>{values.join(', ')}</span>
              </List.Item>
          )}          
        </List>
      </List.Item>
      <List.Item>
        <div><b>Content:</b></div>
        <List>
          {Object.entries(response.content).map(([key, value]) => 
              <List.Item key={key}>
                <b>{key}</b>:&nbsp;
                <span className={calculateDiffClass(diff, 'content', key)}>{value}</span>
              </List.Item>
          )}          
        </List>
      </List.Item>
    </List> 
  );
};


const DiffRecordRow = ({ record }) => {
  const [isOpen, setIsOpen] = useState(false);
  const handleToggle = () => setIsOpen(!isOpen);

  const toggleStyle = {
    display: isOpen ? "table-row" : "none"
  };

  const rowClassMap = {'delete': 'negative', 'insert': 'positive', 'diff': 'warning', 'equal': ''};
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
        />      
      </Tab.Pane>
    )},
  ] : [];

  const ADiffTab = () => <Tab panes={aPanes} />;

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
        />      
      </Tab.Pane>
    )},
  ] : [];

  const BDiffTab = () => <Tab panes={bPanes} />;

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
          {record.pair.a && <ADiffTab />}
        </Table.Cell>
        <Table.Cell colSpan={1} className="entry-data">
          {record.pair.b && <BDiffTab />}
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
        <Header icon='list' content='All' subheader='Shows all compared hars records' onClick={() => setFilterType('')}/>
      ),
    },
    {
      key: 2,
      text: 'Added',
      value: 2,
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
      key: 3,
      text: 'Removed',
      value: 3,
      content: (
        <Header
          icon='minus'
          content='Removed'
          subheader='Shows all removed records from second har'
          onClick={() => setFilterType('removed')}          
        />
      ),
    },
    {
      key: 3,
      text: 'Modified',
      value: 3,
      content: (
        <Header
          icon='exchange'
          content='Modifed'
          subheader='Shows all modified records'
          onClick={() => setFilterType('modified')}          
        />
      ),
    },    
  ];
  return <Dropdown selection fluid options={options} placeholder='Filter' />;
}


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      filterName: null,
      records: [],
    }
    fetch('./data.json').then(response => {
          return response.json();
        }).then(data => {
          this.setState({
            records: data,
          })
        }).catch(err => {
          console.log("Error Reading data " + err);
        });
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
    };
    return records;
  }

  render() {
    let {
      records
    } = this.state;
    if (this.state.filterName) {
      records = this.filterRecords();
    }

    return (
      <Container>
        <Header as='h1' dividing>Harnic</Header>
        <FilterDropdown setFilterType={this.setFilterType}/>
        <Table fixed celled selectable>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Har1</Table.HeaderCell>
              <Table.HeaderCell>Har2</Table.HeaderCell>
            </Table.Row>
          </Table.Header>

          <Table.Body>
              {records.map(record => 
                record && <DiffRecordRow record={record}/>           
                // <Fragment>
                //   <Table.Row className={rowClassMap[record.tag]}>
                    // <Table.Cell>
                    //   {record.pair.a && 
                    //     <Fragment>
                    //       <Label
                    //         size='mini'
                    //         color={reqMethodClassMap[record.pair.a.request.method.toLowerCase()]}
                    //         basic
                    //       >
                    //         {record.pair.a.request.method}
                    //       </Label>&nbsp;&nbsp;
                    //       {truncate(record.pair.a.request.url.url, 150)}
                    //     </Fragment>
                    //   }
                    // </Table.Cell>
                    // <Table.Cell>
                    //   {record.pair.b && 
                    //     <Fragment>
                    //       <Label
                    //         size='mini'
                    //         color={reqMethodClassMap[record.pair.b.request.method.toLowerCase()]}
                    //         basic
                    //       >
                    //         {record.pair.b.request.method}
                    //       </Label>&nbsp;&nbsp;
                    //       {truncate(record.pair.b.request.url.url, 150)}
                    //     </Fragment>
                    //   }
                    // </Table.Cell>
                //   </Table.Row>
                //   <Table.Row style={toggleStyle}>
                //     <Table.Cell colSpan={2}>
                //       Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quidem quod
                //       nam delectus voluptatum rem iure vero, eligendi repellat veniam
                //       voluptatem veritatis dolores, enim animi tempore dolorem nulla fuga
                //       minus repudiandae aliquam! Perferendis aut tempore provident, error
                //       quidem nesciunt atque? Soluta aliquam quisquam deserunt, facere
                //       voluptas odio commodi architecto asperiores sapiente.
                //     </Table.Cell>
                //   </Table.Row>
                // </Fragment>
              )}
          </Table.Body>      
        </Table>
      </Container>
    );
  }
}

export default App;
