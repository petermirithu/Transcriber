# -*- coding: utf-8 -*-
from attrdict import AttrDict


class Account(object):
    """Account management.

    https://fleep.io/fleepapi/ref-account.html
    """
    def __init__(self, server, handler='account'):
        self._server = server
        self._handler = handler

        self.smtp = AttrDict({
            'configure': self.smtp_configure,
            'list': self.smtp_list,
            'store': self.smtp_store})

    def register(self, email, display_name, password, referer=None):
        """Create new account and send verification email.

        :param email: Email.
        :param display_name: Name to be displayed in conversations.
        :param password: Initial password to set.
        :param referer: Optional. Page that referred user to Fleep.
        """
        response = self._server.post(
            "account/register",
            {'email': email, 'display_name': display_name,
             'password': password, 'referer': referer})
        return response

    def reset_password(self, email):
        """Request password reset email for active account.
        Password is not reset yet just email with rest token is sent out.
        User must click on link in email and then enter new passord to rest it.

        :param email: The email.
        """
        return self._server.post("account/reset_password", {'email': email})

    def login(self, email, password, remember_me=False):
        """Handle user login business logic.
        If login is successful, it sets session token and returns account info.

        :param email: The email.
        :param password: User password.
        :param remember_me: Whether user wants long-term session cookie.
        Defaults to False.
        :returns: Response data contains:

            account_id    text  - internal account id
            display_name  text  - name to be displayed in conversations
            profiles      list  - stream of ContactInfo records
            ticket        text  - Must be sent as parameter to all
                                  subsequent api calls
        """
        return self._server.login(email, password, remember_me)

    def logout(self):
        """Close session.
        """
        return self._server.logout()

    def poll(self, event_horizon=0, wait=True, poll_flags=None):
        """
        :param event_horizon: latest event client has seen
        :param wait: Set to False if you want to get latest events
        but not stay waiting if there isn't any
        :param poll_flags: A list of strings that can be used to fine
        tune polls according to client needs. See possible values:
            skip_hidden - skip hidden conversations during initial sync.
            skip_rest   - skip other conversations and start polling events
                          used for limiting number of conversations loaded
                          into client cache
        """
        data = {
            'wait': wait,
            'event_horizon': event_horizon,
            'poll_flags': poll_flags}

        return self._server.post("account/poll", data)

    def listen(self, event_horizon, download_url, wait=True):
        """

        :param event_horizon:
        :param download_url:
        :param wait: Defaults to True.
        """
        return self._server.post(
            'account/listen',
            {'event_horizon': event_horizon,
             'download_url': download_url,
             'wait': wait})

    def sync(self, event_horizon, email, display_name,
             account_id, mk_account_status):
        """Use it to initialize some information using token.

        :param event_horizon: no point to read historic events either
        server must return good enough guess so that contacts and
        conversations will be in good enough order
        :param email: Account's email
        :param display_name: Account's display name.
        :param account_id: Account ID
        :param mk_account_status: See Classificators
        """
        return self._server.post(
            'account/sync',
            {'event_horizon': event_horizon,
             'email': email,
             'display_name': display_name,
             'account_id': account_id,
             'mk_account_status': mk_account_status})

    def sync_conversations(self, conversation_ids=None, sync_cursor=None,
                           label=None, label_id=None, mk_init_mode='ic_tiny'):
        """Get next or previous batch of conversations

        :param conversation_ids: List of conversations IDs to sync
        :param sync_cursor: Cursor received from server w/ previous sync call.
        :param label: Get conversations for one label sorted by last visible
        message time. Options: 'Unread', 'Muted', 'Recent', 'Archived'.
        :param label_id: Get conversations for one label.
        :param mk_init_mode: ic_tiny for minimal or ic_full for display.
        """
        return self._server.post(
            'account/sync_conversations',
            {'conversation_ids': conversation_ids,
             'sync_cursor': sync_cursor,
             'label': label,
             'label_id': label_id,
             'mk_init_mode': mk_init_mode})

    def configure(self, **kwargs):
        """Change account related settings.

        :param display_name: Name displayed instead of email in chats
        :param old_password: Required when submitting new password
        :param password: New password
        :param phone_nr: User's phone number
        :param email_interval: Email interval
        :param is_full_privacy: Stop sending out reading writing activity
        :param is_newsletter_disabled: Enable/disable newsletter sending
        :param is_automute_enabled: Enable/disable incoming email automute
        :param client_settings: json encoded dict of changed client settings
        :param primary_email: Set new primary email (it has to be confirmed
        as alias first)
        """

        if (('old_password' in kwargs and 'password' not in kwargs) or
                ('password' in kwargs and 'old_password' not in kwargs)):
            raise ValueError('Both old_password and password must be present.')

        return self._server.post('account/configure', kwargs)

    def confirm(self, notification_id):
        """Use to confirm account creation.

        :param notification_id: The ID that you receive via email
        on the confirmation URL.
        """
        return self._server.post('account/confirm', notification_id)

    def export_start(self, export_action='history_all', conversation_id=None):
        """Export conversation history.
        User is notified when files are available for download.

        :param export_action: What to export: Defaults to
        history_all - conversation history, all file types.
        :param conversation_id: If set, generate files for this
        conversation only.
        """
        return self._server.post(
            'account/export/start',
            {'export_action': export_action,
             'conversation_id': conversation_id})

    def set_flag(self, client_flag, bool_value=True):
        """Set flag for given account that may be used by clients
        to display or hide content etc

        :param client_flag: name of the flag to set or clear
        :param bool_value: clear given flag from account.
        """
        return self._server.post(
            'account/set_flag',
            {'client_flag': client_flag, 'bool_value': True})

    def smtp_configure(self, smtp_id, smtp_username=None, smtp_password=None,
                       smtp_host=None, smtp_port=None, is_removed=None,
                       is_default_boolean=None):
        """
        :param smtp_id: UUID.
        :param smtp_username: The SMTP server username.
        :param smtp_password: The SMTP password.
        :param smtp_host: The SMTP server host.
        :param smtp_port: SMTP port, set to -1 to remove.
        :param is_removed: set True to remove
        :param is_default: Set True to set as default
        """
        return self._server.post('account/smtp/configure')

    def smtp_list(self):
        """Lists SMTP servers related to account.
        """
        return self._server.post('account/smtp/list')

    def smtp_store(self):
        """
        """
        raise NotImplementedError
