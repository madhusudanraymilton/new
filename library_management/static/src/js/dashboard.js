/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class LibraryDashboard extends Component {
    static template = "library_management.LibraryDashboard";
}

registry.category("actions").add("library_dashboard", LibraryDashboard);