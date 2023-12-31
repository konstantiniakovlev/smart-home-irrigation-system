-- create device and program registry tables
create table device_registry (
    device_id int generated always as identity,
    mac_address macaddr not null,
    ip_address cidr not null,
    device_type varchar(255) not null,
    description varchar(255)
);

create table program_registry (
    program_id int generated always as identity,
    device_id int,
    port int not null,
    description varchar(255)
);

-- fill in the tables with initial info
insert into device_registry (
    mac_address,
    ip_address,
    device_type,
    description
)
values (
    'd8:3a:dd:3f:6d:a4',
    '192.168.178.179',
    'Raspberry Pi 4 Model B 1GB',
    'Main controller for smart home systems'
);

insert into program_registry (device_id, port, description)
values
    (1, 5431, 'smart-home-timescaledb, postgres extension for time series data'),
    (1, 5432, 'smart-home-postgres, postgres for devices used in house'),
    (1, 5000, 'smart-home-irrigation-system-api, api to control irrigation devices');
