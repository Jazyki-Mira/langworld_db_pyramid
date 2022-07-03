import DoculectListItem from "./doculectListItem.js"

const retrieve_data = url => fetch(url)
        .then(res => res.json())
        .then(renderListOfMatchingDoculects)
        .catch(console.error);

const renderListOfMatchingDoculects = retrieved_data => {

    if (typeof retrieved_data[Symbol.iterator] != 'function') return;  // promise is pending, no data to iterate over

    ReactDOM.render(
        React.createElement(
            'ul',
            {},
            retrieved_data.map(
                (item, i) => React.createElement(
                    DoculectListItem, { doculect: item, key: i }, null
                    )
                )
            ),
        document.getElementById("doculect-finder-list")
        );
}

function DoculectListForm(props) {
    const [query, setQuery] = React.useState("");

    const handleSubmit = (e) => {
      e.preventDefault();
//      console.log(query);
      let url = "/ru/json_api/doculect_by_name/" + query
      renderListOfMatchingDoculects(retrieve_data(url));
    }

    return React.createElement(
        "form",
        { onSubmit: e => {handleSubmit(e)} },
        React.createElement("label", {}, "Поиск языка"),
        React.createElement("br"),
        React.createElement("input", {name: "searchText", type: "text", onChange: e => setQuery(e.target.value)}),
        React.createElement("input", {type: "submit", value: "Поиск подходящих языков"})
    )
}

ReactDOM.render(React.createElement(DoculectListForm), document.getElementById("doculect-finder-form"));
