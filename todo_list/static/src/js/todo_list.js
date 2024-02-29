/** @odoo-module */

import { Component } from "@odoo/owl";

export class TodoList extends Component{
    setup() {
        this.todo_list = {
            id:3,
            description: "buy milk",
            done: true
        };
    }
}
TodoList.template = "todo_list_template"