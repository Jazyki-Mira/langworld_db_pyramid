import getLocale from "./getLocale.js"

const retrieve_data = url => fetch(url)
        .then(res => res.json())
        .then(renderGenealogyTree)
        .catch(console.error);


const createTree = (items, typeOfItem = "family") => {
    return React.createElement(
            "ul",
            {},
            items.map(item => {
                let elementContents  = null;
                switch (typeOfItem) {
                    case "family": 
                        elementContents = [item["name"]];
                        break;
                    case "doculect":
                        elementContents = [React.createElement('a', { href: `../doculect/${item["id"]}` }, item["name"])];
                        break;
                }

                if ("children" in item && item["children"].length > 0) elementContents.push(createTree(item["children"]));
                if ("doculects" in item && item["doculects"].length > 0) elementContents.push(createTree(item["doculects"], "doculect"));
                
                return React.createElement("li", { key: item["id"], className: typeOfItem }, ...elementContents);
            })
        )
}

const renderGenealogyTree = retrieved_data => {

    if (typeof retrieved_data[Symbol.iterator] != 'function') return;  // promise is pending, no data to iterate over
    
    ReactDOM.render(createTree(retrieved_data), document.getElementById("genealogy-tree"));
}

const genealogyUrl = "/" + getLocale() + "/json_api/genealogy";
retrieve_data(genealogyUrl);
