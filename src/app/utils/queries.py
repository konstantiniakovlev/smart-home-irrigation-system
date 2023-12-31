get_devices_query = """
select 
pr.device_id,
pr.port,
dr.device_id,
dr.mac_address,
dr.ip_address, 
dr.device_type,
pr.description
from program_registry as pr
inner join device_registry as dr
on pr.device_id = dr.device_id;
"""

get_device_query = """
select 
pr.device_id,
pr.port,
dr.device_id,
dr.mac_address,
dr.ip_address, 
dr.device_type,
pr.description
from program_registry as pr
inner join device_registry as dr
on pr.device_id = dr.device_id
where dr.device_id = '%(device_id)s';
"""

register_device_query = """
update device_registry set ip_address='%(ip_address)s', device_type='%(device_type)s', description='%(description)s'
where mac_address='%(mac_address)s';
insert into device_registry (mac_address, ip_address, device_type, description)
select '%(mac_address)s', '%(ip_address)s', '%(device_type)s', '%(description)s'
 where not exists (select 1 from device_registry where mac_address='%(mac_address)s');
 select device_id from device_registry where mac_address='%(mac_address)s';
"""

register_program_query = """
update program_registry set description='%(description)s'
where device_id='%(device_id)s' and port='%(port)s';
insert into program_registry (device_id, port, description)
select '%(device_id)s', '%(port)s', '%(description)s'
 where not exists (select 1 from program_registry where device_id='%(device_id)s' and port='%(port)s');
"""