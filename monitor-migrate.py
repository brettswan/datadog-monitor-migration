#!/usr/bin/env python
from datadog import initialize, api

def initialize_dd_api(account):
    options = {
        'api_key': configs[account]["api_key"],
        'app_key': configs[account]["app_key"]
    }

    initialize(**options)

class Monitor:
    def __init__(self,type,query,name,message,tags,options):
        self.type = type
        self.query = query
        self.name = name
        self.message = message
        self.tags = tags
        self.options = options

    def print_monitor(self):
        print("\n\n{}".format(self.__dict__))

    def create_monitor(self):
        create_monitor_request = api.Monitor.create(
            type = self.type,
            query = self.query,
            name = self.name,
            message = self.message,
            tags = self.tags,
            options = self.options
        )
        return create_monitor_request

configs = {
    "SOURCE_ACCOUNT" : {
        "api_key" : "SOURCE_ACCOUNT_API_KEY",
        "app_key" : "SOURCE_ACCOUNT_APP_KEY"
    },
    "DEST_ACCOUNT" : {
        "api_key" : "DEST_ACCOUNT_API_KEY",
        "app_key" : "DEST_ACCOUNT_APP_KEY"
    }
}

initialize_dd_api("SOURCE_ACCOUNT")

monitors = api.Monitor.get_all()

initialize_dd_api("DEST_ACCOUNT")

for m in monitors:
    new_monitor = Monitor(
        type = m["type"],
        query = m["query"],
        name = m["name"],
        tags = m["tags"],
        options = m["options"],
        message = m["message"]
        )
    new_monitor.print_monitor()
    new_monitor.create_monitor()
    del new_monitor
