# langworld_db_pyramid
Languages of the World Database as a [Pyramid](https://trypyramid.com/) web app.

The data is pulled via `git subtree` from a
data repository into [*langworld_db_data*](langworld_db_data). The actual data files are in [*data*](langworld_db_data/data) subdirectory of that package.
See the [Entity Relationship Diagram](langworld_db_pyramid/dbutils/erd.png) of the relational database that was generated from the data for the web app.

The [*langworld_db_pyramid*](langworld_db_pyramid)
package contains the actual Pyramid web app. The tests
for this package are stored in a [separate directory](tests).
