# FILE: models/hr_leave.py
# ============================================================
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # Override state to include validate1
    state = fields.Selection(selection_add=[
        ('validate1', 'Team Leader Approved'),
    ], ondelete={'validate1': 'set default'})

    # Track who approved at each level
    team_leader_approved_by = fields.Many2one(
        'res.users',
        string='Team Leader Approved By',
        readonly=True,
        tracking=True
    )
    team_leader_approved_date = fields.Datetime(
        string='Team Leader Approval Date',
        readonly=True,
        tracking=True
    )
    hr_approved_by = fields.Many2one(
        'res.users',
        string='HR Approved By',
        readonly=True,
        tracking=True
    )
    hr_approved_date = fields.Datetime(
        string='HR Approval Date',
        readonly=True,
        tracking=True
    )

    def _check_approval_access(self, approval_level):
        """
        Check if current user has permission to approve at given level
        approval_level: 'team_leader' or 'hr'
        """
        self.ensure_one()
        user = self.env.user

        # Administrators can always approve
        if user.has_group('two_layer_timeoff_approval.group_timeoff_administrator'):
            return True

        if approval_level == 'team_leader':
            # Team Leader approval
            if user.has_group('two_layer_timeoff_approval.group_team_leader'):
                # Check if user is the manager of the employee
                if self.employee_id.parent_id and self.employee_id.parent_id.user_id.id == user.id:
                    return True
            return False

        elif approval_level == 'hr':
            # HR Manager approval
            if user.has_group('two_layer_timeoff_approval.group_hr_manager'):
                return True
            return False

        return False

    def action_approve_team_leader(self):
        """Team Leader Approval - First Layer"""
        for leave in self:
            # Check if in correct state
            if leave.state != 'confirm':
                raise UserError(_(
                    'Time off request must be in "To Approve" state for Team Leader approval.'
                ))

            # Check access rights
            if not leave._check_approval_access('team_leader'):
                raise UserError(_(
                    'You do not have permission to approve this time off request as Team Leader. '
                    'You must be the direct manager of the employee.'
                ))

            # Approve
            leave.write({
                'state': 'validate1',
                'team_leader_approved_by': self.env.user.id,
                'team_leader_approved_date': fields.Datetime.now(),
            })

            # Log message
            leave.message_post(
                body=_('Time off request approved by Team Leader: %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment'
            )

        return True

    def action_approve_hr(self):
        """HR Manager/Admin Approval - Second Layer (Final)"""
        for leave in self:
            # Critical: Check if Team Leader has approved first
            if leave.state != 'validate1':
                raise UserError(_(
                    'Time off request must be approved by Team Leader first '
                    '(state must be "Team Leader Approved").'
                ))

            # Check access rights
            if not leave._check_approval_access('hr'):
                raise UserError(_(
                    'You do not have permission to give final approval for this time off request.'
                ))

            # Final approval - call parent's validation method
            leave.write({
                'hr_approved_by': self.env.user.id,
                'hr_approved_date': fields.Datetime.now(),
            })

            # Call the standard Odoo approve method
            # This handles state change, allocation, notifications, etc.
            leave.action_validate()

            # Log message
            leave.message_post(
                body=_('Time off request finally approved by HR/Admin: %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment'
            )

        return True

    def action_refuse(self):
        """Refuse the time off request"""
        for leave in self:
            # Check if user has permission to refuse
            user = self.env.user
            can_refuse = False

            if user.has_group('two_layer_timeoff_approval.group_timeoff_administrator'):
                can_refuse = True
            elif user.has_group('two_layer_timeoff_approval.group_hr_manager'):
                can_refuse = True
            elif user.has_group('two_layer_timeoff_approval.group_team_leader'):
                # Team leader can refuse if they are the manager
                if leave.employee_id.parent_id and leave.employee_id.parent_id.user_id.id == user.id:
                    can_refuse = True

            if not can_refuse:
                raise UserError(_(
                    'You do not have permission to refuse this time off request.'
                ))

            # Log message before refusing
            leave.message_post(
                body=_('Time off request refused by: %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment'
            )

            # Call parent's refuse method
            super(HrLeave, leave).action_refuse()

        return True

    def action_confirm(self):
        """Override to set state to confirm"""
        res = super(HrLeave, self).action_confirm()
        # Ensure state is 'confirm' not 'validate1' or 'validate'
        for leave in self:
            if leave.state == 'validate':
                leave.write({'state': 'confirm'})
        return res

    def action_validate(self):
        """Override to prevent direct approval without team leader"""
        for leave in self:
            # If trying to validate directly without team leader approval
            if leave.state == 'confirm' and not leave.team_leader_approved_by:
                # Check if user is admin - they can bypass
                if self.env.user.has_group('two_layer_timeoff_approval.group_timeoff_administrator'):
                    # Admin can approve directly
                    leave.write({
                        'team_leader_approved_by': self.env.user.id,
                        'team_leader_approved_date': fields.Datetime.now(),
                        'hr_approved_by': self.env.user.id,
                        'hr_approved_date': fields.Datetime.now(),
                    })
                else:
                    raise ValidationError(_(
                        'Cannot approve time off request without Team Leader approval first. '
                        'Please use the two-layer approval workflow.'
                    ))

            # If in validate1 state, must go through HR approval
            if leave.state == 'validate1':
                raise UserError(_(
                    'Please use the "Final Approve (HR)" button for HR approval.'
                ))

        return super(HrLeave, self).action_validate()

    @api.constrains('state')
    def _check_state_transition(self):
        """Validate state transitions"""
        for leave in self:
            # Allow admin to bypass this check
            if self.env.user.has_group('two_layer_timeoff_approval.group_timeoff_administrator'):
                continue

            # Ensure validate1 comes before validate
            if leave.state == 'validate' and not leave.team_leader_approved_by:
                raise ValidationError(_(
                    'Cannot approve time off request without Team Leader approval first.'
                ))