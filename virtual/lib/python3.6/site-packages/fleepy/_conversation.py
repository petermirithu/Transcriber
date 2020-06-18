# -*- coding: utf-8 -*-
class Conversation(object):
    """Conversation management.

    https://fleep.io/fleepapi/ref-conversation.html
    """
    def __init__(self, server, handler='conversation'):
        self._server = server
        self._handler = handler

    def call(self, *args, **kwargs):
        """
        """
        if 'method' in kwargs:
            requester_func = getattr(self._server, kwargs.pop('method'))
        else:
            requester_func = self._server.post

        return requester_func(*args, **kwargs)

    def add_members(self, emails, from_message_nr=None):
        """Add members to the conversation

        :param emails: A list of emails.
        :param from_message_nr: Used to return next batch of changes.
        """
        emails = '; '.join(emails)
        return self.call(
            'conversation/add_members',
            {'emails': emails, 'from_message_nr': from_message_nr})

    def autojoin(self, conv_url_key):
        """Autojoin conversation if not member yet.
        Autojoin url has following format https://fleep.io/chat/<conv_url_key>

        :param conv_url_key: Last part of autojoin url or conversation_id
        """
        return self.call(
            'conversation/autojoin', {'conv_url_key': conv_url_key})

    def check_permissions(self, conversation_id):
        """Check if account has modification rights on the conversation.
        Same check is done in all conversation services so this here mainly
        helps with testing and documentation at first.

        :param conversation_id: The conversation id.
        """
        return self.call(
            'conversation/check_permissions/{}'.format(conversation_id))

    def create(self, topic=None, emails=None, message=None,
               attachments=None, is_invite=None):
        """Create new conversation

        :param topic: Conversation topic. Optional.
        :param emails: A list of emails. Optional.
        :param message: Initial message. Optional.
        :param attachments: list of AttachmentInfos to be added to
        conversation. Optional.
        :param is_invite: Send out invite emails to fresh fleepers.
        Defaults to None.
        """
        emails = '; '.join(emails)
        return self.call(
            'conversation/create',
            {'topic': topic, 'emails': emails, 'message': message,
             'attachments': attachments, 'is_invite': is_invite})

    def create_hangout(self, conversation_id):
        """Create a new hangout.
        """
        return self.call(
            'conversation/create_hangout/{}'.format(conversation_id))

    def delete(self, conversation_id):
        """Remove conversation from your conversation list.
        If you don’t leave conversation before deleting it will
        still reappear when someone writes in it.
        """
        return self.call(
            'conversation/delete/{}'.format(conversation_id))

    def _disclose(self, endpoint, conversation_id, emails, **kwargs):
        """
        """
        kwargs['emails'] = ';'.join(emails)
        return self.call('conversation/{}/{}', kwargs)

    def disclose(self, conversation_id, emails,
                 message_nr=None, from_message_nr=None):
        """Disclose conversation history to members until given message.
        :param conversation_id: The conversation id.

        :param emails: A list of emails.
        :param message_nr: disclose up to this message
        :param from_message_nr: used to return next batch of changes
        """
        return self._disclose(
            'disclose', conversation_id, emails,
            {'message_nr': message_nr, 'from_message_nr': from_message_nr})

    def disclose_all(self, conversation_id, emails, from_message_nr=None):
        """Disclose conversation history to members. All content of last
        membership is disclosed.
        """
        return self._disclose(
            'disclose_all', conversation_id, emails,
            {'from_message_nr': from_message_nr})

    def hide(self, conversation_id, from_message_nr=None):
        """Hide conversation until new messages arrives.
        Useful for people who want to keep their inbox clear.
        """
        return self.call('conversation/hide/{}'.format(
            conversation_id), {'from_message_nr': from_message_nr})

    def label(self, label, sync_horizon=None):
        """List all conversations with that label.
        """
        return self.call(
            'conversation/label',
            {'label': label, 'sync_horizon': sync_horizon})

    def leave(self, conversation_id, from_message_nr=None):
        """Leaves the conversation.
        """
        return self.call('conversation/leave/{}'.format(
            conversation_id), {'from_message_nr': from_message_nr})

    def list(self, sync_horizon=None):
        """List all conversations for this account.
        Same conversations may pop up several times due to shifting order
        caused by incoming messages. Stop calling when you receive empty
        conversation list.
        """
        return self.call(
            'conversation/list', {'sync_horizon': sync_horizon})

    def mark_read(self, conversation_id, mk_init_mode='ic_tiny'):
        """Mark conversation as read regardless of how many unread messages
        there are. Useful for marking read conversations that you are not
        planning to read.

        For example error log after it has rolled up thousands of messages.
        Returns init conversation stream so the client side conversation will
        be reset to new read position and all the possibly skipped messages
        will not get misinterpreted.

        :param mk_init_mode: ic_tiny or ic_full. Defaults to ic_tiny.
        """
        return self.call(
            'conversation/mark_read/{}'.format(conversation_id),
            {'mk_init_mode': mk_init_mode})

    def poke(self, conversation_id, message_nr, from_message_nr, is_bg_poke):
        """Send poke event, used for testing sync between clients.
        """
        data = {
            'message_nr': message_nr,
            'from_message_nr': from_message_nr,
            'is_bg_poke': is_bg_poke}

        return self.call(
            'conversation/poke/{}'.format(conversation_id), data)

    def remove_members(self, conversation_id, emails, from_message_nr=None):
        """Remove members from the conversation.

        :param conversation_id: The ID of the conversation that members should
        be removed.
        :param emails: A list of emails.
        :param from_message_nr: Used to return next batch of changes.
        """
        emails = '; '.join(emails)
        return self.call(
            'conversation/remove_members/{}'.format(conversation_id),
            {'emails': emails, 'from_message_nr': from_message_nr})

    def set_alerts(self, conversation_id, mk_alert_level,
                   from_message_nr=None):
        """Set conversation alerts.
        """
        if mk_alert_level not in ('default', 'never'):
            raise ValueError('alert level should be default or never')

        data = {
            'mk_alert_level': mk_alert_level,
            'from_message_nr': from_message_nr}
        return self.call(
            'conversation/set_alerts/{}'.format(conversation_id), data)

    def set_topic(self, conversation_id, topic, from_message_nr=None):
        """Change conversation topic.
        """
        data = {'topic': topic, 'from_message_nr': from_message_nr}
        return self.call(
            'conversation/set_topic/{}'.format(conversation_id), data)

    def show_activity(self, conversation_id, is_writing, message_nr=None):
        """Show writing pen and/or pinboard editing status. This works both ways.
        Any call activates this conversation for this account.
        So to start receiving activity call with empty parameters.
        """
        return self.call(
            'conversation/set_topic/{}'.format(conversation_id),
            {'is_writing': is_writing, 'message_nr': message_nr})

    def slash_command(self, conversation_id, message, from_message_nr=None):
        """Slash commands for conversations
        """
        return self.call(
            'conversation/slash_command/{}'.format(conversation_id),
            {'message': message, 'from_message_nr': from_message_nr})

    def store(self, conversation_id, **kwargs):
        """Store conversation header fields. Store only fields that have
        changed. Call only when cache is fully synced.

        :param conversation_id: The conversation id.

        Params allowed in kwargs:

        :param read_message_nr: New read horizon for conversation
        :param labels: User labels for conversation
        :param topic: Shared topic for conversation
        :param mk_alert_level: User alert level for the conversation
        :param snooze_interval: For how long to snooze conversation in seconds
        :param add_emails: emails of members to be added
        :param remove_emails: emails of members to be removed
        :param disclose_emails: disclose conversation to these users
        :param add_ids: add emails (as given, no mapping)
        :param remove_ids: remove emails (as given, no mapping)
        :param disclose_ids: disclose chat to given accounts
        :param hide_message_nr: Hide the conversation from this message nr
        :param is_deleted: Set to true to delete the conversation
        :param from_message_nr: used to return next batch of changes
        :param is_autojoin: enable disable auto join
        :param is_disclose: enable/disable auto disclose
        :param can_post: set to false to leave the conversation
        :param is_url_preview_disabled: don't show url previews for all users
        """
        allowed_parameters = (
            'read_message_nr', 'labels', 'topic', 'mk_alert_level',
            'snooze_interval', 'add_emails', 'remove_emails',
            'disclose_emails', 'add_ids', 'remove_ids', 'disclose_ids',
            'hide_message_nr', 'is_deleted', 'from_message_nr', 'is_autojoin',
            'is_disclose', 'can_post', 'is_url_preview_disabled')

        for key in kwargs:
            if key not in allowed_parameters:
                raise ValueError('{} is not a valid paramater'.format(key))

        return self.call(
            'conversation/store/{}'.format(conversation_id), kwargs)

    def sync(self, conversation_id, from_message_nr=None, mk_direction=None):
        """Sync state for single conversation. If used with default values 5
        messages before and after last reported read_message_nr are returned.
        Also all conversation state are returned: PinInfo, memberInfo. All
        optional fields (o) are returned for first sync. After that these are
        included only when there have been changes. Changes are detected from
        system messages in message flow.

        :param from_message_nr: last message nr client has received.
        :param mk_direction: ic_tiny - do minimal init conversation
                                       returns only inbox message and header
                             ic_full - do full init conversation
                                       returns inbox message and several
                                       messages before and after current
                                       read horizon and several pins and
                                       several files
                             ic_flow - get flow fragment
                                       returns several messages before and
                                       after given from_message_nr or current
                                       read horizon if from message nr
                                       not given
                             ic_end - get flow fragment from the end
                                      of all available content
                             ic_backward - get flow fragment before given
                                           message
                             ic_forward - get flow fragment after given message
                                          only visible messages are returned so
                                          not suitable for syncing cached
                                          conversation (edits will be lost)
                             ic_files - get only messages with files.
                             ic_pinboard - get only shared messages.
                             ic_tasks -get only archeved task messages.
                             <null> - default behaviour get sequential
                               messages forward. Returns all flow messages even
                               non visible ones like edits of older messages
        """
        return self.call(
            'conversation/sync/{}'.format(conversation_id),
            {'from_message_nr': from_message_nr, 'mk_direction': mk_direction})

    def _sync(self, sync_type, conversation_id, from_message_nr=None):
        return self.call(
            'conversation/sync_{}/{}'.format(sync_type, conversation_id),
            {'from_message_nr': from_message_nr})

    def sync_backward(self, conversation_id, from_message_nr=None):
        """Sync state for single conversation. Used to fetch messages for
        backward scroll.
        """
        return self._sync('backward', conversation_id, from_message_nr)

    def sync_files(self, conversation_id, from_message_nr=None):
        """Sync earlier files if user wants to browse them
        """
        return self._sync('files', conversation_id, from_message_nr)

    def sync_pins(self, conversation_id, from_message_nr=None):
        """Sync pinboard for conversation where it was not fully sent with init
        """
        return self._sync('pins', conversation_id, from_message_nr)

    def unhide(self, conversation_id, from_message_nr=None):
        """Bring conversation out of hiding
        """
        return self.call(
            'conversation/unhide/{}'.format(conversation_id),
            {'from_message_nr': from_message_nr})

    def configure_hook(self, conversation_id, hook_key,
                       hook_name=None, from_message_nr=None):
        """Change hook name and/or other settings.
        """
        return self.call(
            'conversation/configure_hook/{}'.format(conversation_id),
            {'hook_key': hook_key,
             'hook_name': hook_name,
             'from_message_nr': from_message_nr})

    def create_hook(self, conversation_id, hook_name=None,
                    mk_hook_type='plain', from_message_nr=None):
        """Create hook for given conversation.

        :param hook_name: Name for hook.
        :param mk_hook_type: plain, jira, github, import, pivotaltracker,
        newrelic, bitbucket, zapier, confluence, gitlab, sameroom.
        :param from_message_nr: Used to return next batch of messages.
        """
        return self.call(
            'conversation/create_hook/{}'.format(conversation_id),
            {'hook_name': hook_name,
             'mk_hook_type': mk_hook_type,
             'from_message_nr': from_message_nr})

    def drop_hook(self, conversation_id, hook_key, from_message_nr=None):
        """Remove hook from conversation.
        """
        return self.call(
            'conversation/drop_hook/{}'.format(conversation_id),
            {'hook_key': hook_key,
             'from_message_nr': from_message_nr})

    def show_hooks(self, conversation_id):
        """Show hooks in converastion.
        :param conversation_id: The conversation ID.
        """
        return self.call('conversation/show_hooks/{}'.format(conversation_id))
