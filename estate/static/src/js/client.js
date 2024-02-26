/** @odoo-module **/

import { registry } from "@web/core/registry";

import { Component } from  "@odoo/owl";

class MyClientAction extends Component {}
MyClientAction.template = "estate.clientaction";

// remember the tag name we put in the first step
registry.category("actions").add("estate.MyClientAction", MyClientAction);