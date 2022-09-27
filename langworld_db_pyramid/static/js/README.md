The files in the root of this directory are scripts that are included into [Jinja templates](/langworld_db_pyramid/templates)
with `<script src="..." type="module">`.

Subdirectories contain modules that are used by these
"high-level" scripts. Most notably, [`MapWithList`](mapWithList/MapWithList.js) is
a [React](https://reactjs.org/) Component consisting, in turn, of smaller components that are stored
in [`mapWithList/components`](mapWithList/components).

Others are plain Javascript. The [`slimselect`](slimselect) directory contains minified [SlimSelect](https://slimselectjs.com/) script.