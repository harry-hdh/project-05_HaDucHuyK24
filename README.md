# project-05_HaDucHuyK24
# Glamira Data Pipeline

## Setup GCP with Mongodb

- n2-standard-4 (4 vCPUs, 16 GB memory)
- ubuntu-2204-jammy-v20260530

### GCP Firewall Rule
1. VPC network > Firewall
2. Click **Create Firewall Rule** at the top.
3. Fill in the following details:
- **Name:** `allow-mongodb-from-gcp-instance`
- **Network:** Select the VPC network where your database resides (usually `default`).
- **Direction of traffic:** `Ingress`
- **Action on match:** `Allow`
- **Targets:** Choose `All instances in the network` (or use `Specified target tags` if you only want it applied to a specific database VM).
- **Source filter:** `IPv4 ranges`
- **Source IPv4 ranges:** Paste the IP address you copied in Step 1, adding `/32` to the end to specify that single IP (e.g., `10.128.0.5/32`).
- **Protocols and ports:** Check **Specified protocols and ports**, check **TCP**, and type `27017`.
4. Create

### Install Mongo

### Create user for mongodb
`> mongosh`

`> use admin`

`> db.createUser({
user: "<USERNAME>",
pwd: passwordPrompt(), // This will securely prompt you to type the password safely
roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
})`

### Config Mongodb security
`sudo nano /etc/mongod.conf`

`net:
  port: 27017
  bindIp: 127.0.0.1,<VM_IP>

security:
  authorization: "enabled"`

`sudo systemctl restart mongod`