import DoculectListItem from "./doculectListItem.js"

let url = "http://127.0.0.1:6543/ru/json_api/doculect_by_name/ец";

const render_data = retrieved_data => ReactDOM.render(

    React.createElement(
        'ul',
        {},
        retrieved_data.map(
            (item, i) => React.createElement(
                DoculectListItem, { doculect: item, key: i }, null
                )
            )
        ),
    document.getElementById("doculect-finder")
    );

fetch(url)
    .then(res => res.json())
	.then(render_data)
	.catch(console.error);

