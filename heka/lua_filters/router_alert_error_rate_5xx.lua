require "string"
require "math"
require "table"
require "globals"
local alert = require "alert"
local values = {}
local alert_stack = {}

function process_message ()
    local env = read_message("Fields[Env]")
    -- Create table if not there for env.
    if values[env] == nil then
       values[env] = {}
    end
    local ip = read_message("Fields[IP]")
    -- Create table if not there for IP address.
    if values[env][ip] == nil then
       values[env][ip] = {}
    end
    local response = read_message("Fields[router.responses.5xx]")
    table.insert(values[env][ip], response)
    if table.getn(values[env][ip]) > 100 then
      table.remove(values[env][ip],1)
    end
    local first_value = values[env][ip][1]
    local last_value = values[env][ip][table.getn(values[env][ip])]
    local rate = (last_value - first_value) / first_value * 100
    if rate > 5.0 then
      table.insert(alert_stack, {ip = ip, rate = rate, env = env})
      values[env][ip] = {} -- Reset the array
    end
    return 0
end

function timer_event(ns)
    if table.getn(alert_stack) > 0 then
       local alert_details = alert_stack[1]
       local url = string.format("%s", grafana_host)
       if dashboard_ending[alert_details.env] ~= nil then
           url = string.format("%s/dashboard/db/routing-%s",url, dashboard_ending[alert_details.env])
       end
       local out_message = string.format("<!channel>\n%s's router experiencing high percentage (%.2f %%) of 5xx responses.\nRouter IP: %s\n <%s|Grafana Router Stats>", alert_details.env, alert_details.rate, alert_details.ip, url)
       alert.set_throttle(9e11)
       alert.send(ns, out_message)
       table.remove(alert_stack,1)
    end
end
