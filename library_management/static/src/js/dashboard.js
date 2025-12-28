/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class LibraryDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            data: {
                books: {},
                members: {},
                borrowings: {},
                fines: {},
                top_books: [],
                recent_borrowings: [],
                books_by_category: [],
            },
            loading: true,
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            const data = await this.orm.call(
                "library.dashboard",
                "get_dashboard_data",
                []
            );
            this.state.data = data;
            this.state.loading = false;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.loading = false;
        }
    }

    async openBooks() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.book",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }

    async openAvailableBooks() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.book",
            views: [[false, "list"], [false, "form"]],
            domain: [["available_copies", ">", 0]],
            target: "current",
        });
    }

    async openMembers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.member",
            views: [[false, "kanban"], [false, "list"], [false, "form"]],
            target: "current",
        });
    }

    async openActiveBorrowings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.borrowing",
            views: [[false, "list"], [false, "form"]],
            domain: [["status", "=", "borrowed"]],
            target: "current",
        });
    }

    async openOverdueBorrowings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.borrowing",
            views: [[false, "list"], [false, "form"]],
            domain: [["status", "=", "overdue"]],
            target: "current",
        });
    }

    async openUnpaidFines() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.fine",
            views: [[false, "list"], [false, "form"]],
            domain: [["payment_status", "=", "unpaid"]],
            target: "current",
        });
    }

    async openBorrowing(borrowingId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "library.borrowing",
            views: [[false, "form"]],
            res_id: borrowingId,
            target: "current",
        });
    }
}

LibraryDashboard.template = "library_management.LibraryDashboard";

registry.category("actions").add("library_dashboard", LibraryDashboard);