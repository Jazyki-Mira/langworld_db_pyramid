from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph


def generate_erd(path_to_database: str = "sqlite:///../../langworld_db_pyramid.sqlite") -> None:
    metadata = _prepare_metadata(path_to_database)  # pragma: no cover

    graph = create_schema_graph(
        metadata=metadata, show_indexes=False, rankdir="LR", concentrate="False"
    )
    graph.write_png("erd.png")


def _prepare_metadata(path_to_database: str) -> MetaData:
    """Prepare metadata for further ERD generation.

    1. initialize an engine, 2. reflect DB's metadata, 3. bind all tables' metadata to the engine
    """
    engine = create_engine(path_to_database)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    for table in metadata.tables.values():
        table.metadata.bind = engine
    return metadata


if __name__ == "__main__":
    generate_erd()
