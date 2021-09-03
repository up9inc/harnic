import {
  Header,
  Dropdown,
} from "semantic-ui-react";


const FilterDropdown = ({ setFilterType }) => {
  const options = [
    {
      key: 1,
      text: "All",
      value: 1,
      content: (
        <Header
          icon="table"
          content="All"
          subheader="Shows all compared hars records"
          onClick={() => setFilterType("")}
        />
      ),
    },
    {
      key: 2,
      text: "Changes",
      value: 2,
      content: (
        <Header
          icon="list"
          content="Changes"
          subheader="Shows all records except those that are equal"
          onClick={() => setFilterType("diff")}
        />
      ),
    },
    {
      key: 3,
      text: "Modified entries",
      value: 3,
      content: (
        <Header
          icon="exchange"
          content="Modifed"
          subheader="Shows only modified records"
          onClick={() => setFilterType("modified")}
        />
      ),
    },
    {
      key: 4,
      text: "Added",
      value: 4,
      content: (
        <Header
          icon="plus"
          content="Added"
          subheader="Shows all added records from second har"
          onClick={() => setFilterType("added")}
        />
      ),
    },
    {
      key: 5,
      text: "Removed",
      value: 5,
      content: (
        <Header
          icon="minus"
          content="Removed"
          subheader="Shows all removed records from second har"
          onClick={() => setFilterType("removed")}
        />
      ),
    },
  ];
  return (
    <Dropdown selection fluid floating options={options} placeholder="Filter" />
  );
};

export default FilterDropdown;