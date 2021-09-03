import { Statistic } from "semantic-ui-react";


const Statistics = ({ stats }) => (
  <div className="statistics">
    <Statistic.Group widths="5">
      <Statistic>
        <Statistic.Value>{(stats.ratio * 100).toFixed(1)}%</Statistic.Value>
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
);

export default Statistics;
