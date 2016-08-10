#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import LiarsDiceApi


class SendReminderEmail(webapp2.RequestHandler):
    def post(self):
        """Send a reminder email to a user about the game.
        Called every day using a cron job"""
        app_id = app_identity.get_application_id()
        subject = 'It''s your turn on Liar\'s Dice.'
        body = (
            'Hello {}, your opponent is waiting for your action in game {}.'
            .format(
                self.request.get('user_name'),
                self.request.get('game_key')))
        body += (
            "\n\n{} raised the bid to face: {}, total: {}. Is it a lie?"
            .format(
                self.request.get('bid_player'),
                self.request.get('bid_face'),
                self.request.get('bid_total')))
        # This will send test emails, the arguments to send_mail are:
        # from, to, subject, body
        mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                       self.request.get('email'),
                       subject,
                       body)


app = webapp2.WSGIApplication([
    ('/tasks/send_reminder', SendReminderEmail),
], debug=True)
