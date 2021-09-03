import React, { Component } from "react";
import "semantic-ui-css/semantic.min.css";
import {
  Container,
  Header,
  Table,
  Image,
  Icon,
  Popup,
  Checkbox,
  Grid,
} from "semantic-ui-react";

import DiffRecordRow from "./components/DiffRecordRow.js";
import FilterDropdown from "./components/FilterDropdown.js";
import Statistics from "./components/Statistics.js";
import logo from "./logo.svg";
import "./App.css";


class App extends Component {
  constructor(props) {
    super(props);

    const index = window.globalData.diff.index;
    const original_uuids = window.globalData.diff.strict_order_records;
    const reordered_uuids = window.globalData.diff.reordered_records;

    const strict_order_records = original_uuids.map((rUuid) => index[rUuid]);
    const reordered_records = reordered_uuids.map((rUuid) => index[rUuid]);

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
    }
  }

  setFilterType = (filterName) => {
    this.setState({ filterName: filterName });
  };

  filterRecords = () => {
    const filter = this.state.filterName;
    let records = this.state.records.slice();
    if (filter === "added") {
      records = records.filter((record) => record.pair.a == null);
    } else if (filter === "removed") {
      records = records.filter((record) => record.pair.b == null);
    } else if (filter === "modified") {
      records = records.filter((record) => record.diff && !record.diff.equal);
    } else if (filter === "diff") {
      records = records.filter(
        (record) => !record.diff || (record.diff && !record.diff.equal)
      );
    }
    return records;
  };

  toogleReordered = () => {
    this.setState((prevState) => ({
      showReordered: !prevState.showReordered,
      records: prevState.showReordered
        ? this.state.strict_order_records
        : this.state.reordered_records,
      stats: prevState.showReordered
        ? this.state.kpis.stats.strict_order
        : this.state.kpis.stats.with_reorders,
    }));
  };

  render() {
    let { kpis, records, stats, showReordered, filterName } = this.state;
    if (filterName) {
      records = this.filterRecords();
    }

    const toogleProps = {};
    toogleProps["defaultChecked"] = showReordered;

    return (
      <Container>
        <Container className="header-container">
          <div className="item">
            <Image src={logo} size="small" wrapped />
          </div>
          <div className="item header page-header">
            <Header size="huge">Traffic comparison tool</Header>
          </div>
        </Container>
        <Statistics stats={stats} />
        <Grid>
          <Grid.Row>
            <Grid.Column width={2} className="reorders-toogle">
              <Checkbox
                toggle
                {...toogleProps}
                label="Allow reorders"
                onChange={this.toogleReordered}
              />
              <Popup
                trigger={<Icon name="info" className="reordering-desc-icon" />}
                content="Fixes ordering of the same entries if they were mismatched due to different response time deltas.
                This is mostly caused by the nature of async requests. Those fixed entries have a special icon."
              />
            </Grid.Column>
            <Grid.Column width={14}>
              <FilterDropdown setFilterType={this.setFilterType} />
            </Grid.Column>
          </Grid.Row>
        </Grid>
        <Table fixed celled selectable>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>
                {kpis.file1.path}:&nbsp;&nbsp;{kpis.file1.num_entries} entries
              </Table.HeaderCell>
              <Table.HeaderCell>
                {kpis.file2.path}:&nbsp;&nbsp;{kpis.file2.num_entries} entries
              </Table.HeaderCell>
            </Table.Row>
          </Table.Header>

          <Table.Body>
            {records.map((record) => (
              <DiffRecordRow key={record.id} record={record} />
            ))}
          </Table.Body>
        </Table>
      </Container>
    );
  }
}

export default App;
