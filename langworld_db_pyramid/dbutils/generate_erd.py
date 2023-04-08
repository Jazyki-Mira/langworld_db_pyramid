from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph


def generate_erd(path_to_database: str = "sqlite:///../../langworld_db_pyramid.sqlite") -> None:
    graph = create_schema_graph(
        metadata=MetaData(path_to_database), show_indexes=False, rankdir="LR", concentrate="False"
    )
    graph.write_png("erd.png")


if __name__ == "__main__":
    generate_erd()
