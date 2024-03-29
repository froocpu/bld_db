-- TODO: add metadata/warehousing columns
create table spreadsheets (
    id varchar(44),
    title varchar(255),
    locale varchar(70),
    tz varchar(30),
    url varchar(255),
    author_name varchar(255),
    PRIMARY KEY (id)
);

create table sheets (
    id bigint,
    spreadsheet_id int,
    index int,
    title varchar(255),
    sheet_type char(30),
    row_count int,
    column_count int,
    frozen_row_count int,
    frozen_column_count int,
    PRIMARY KEY (id, spreadsheet_id)
);

create table cells (
    id BIGSERIAL,
    spreadsheet_id char(44),
    sheet_id bigint,
    column_ind int,
    row_ind int,
    range_queried char(15),
    "text" varchar(100),
    PRIMARY KEY (id)
);

create table algorithms (
    id BIGSERIAL,
    spreadsheet_id char(44),
    sheet_id bigint,
    signature char(294), -- up to 7x7x7
    clean_text char(100),
    edges_unsolved_count smallint,
    corners_unsolved_count smallint,
    twisted_corners_count smallint,
    flipped_edges_count smallint,
    parity_flag boolean,
    edge_cycles_count smallint,
    corner_cycles_count smallint,
    comments varchar(255),
    PRIMARY KEY (spreadsheet_id, signature)
);

create table failure_reasons (
    code smallint,
    description varchar(255),
    PRIMARY KEY (id)
);

create table failures (
    id BIGSERIAL,
    spreadsheet_id char(44),
    sheet_id bigint,
    cell_id bigint,
    code int,
    PRIMARY KEY (cell_id, failure_id)
);



