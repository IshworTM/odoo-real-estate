/** @odoo-module */

import { registry } from "@web/core/registry";
import { TodoList } from "./todo_list";
import { Component, useState, mount } from "@odoo/owl";
import { templates } from "@web/core/assets";

export class Counter extends Component{
    setup() {
        this.state = useState({
            value : 0
        });
    }
    
    increment() {
        this.state.value++;
    }
}
mount(TodoList, document.body, { templates, dev: true });
Counter.template = "todo_list.counter_template";
Counter.components = { TodoList };
registry.category("actions").add("todo_list.CounterAction", Counter);