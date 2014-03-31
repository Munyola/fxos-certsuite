# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from semiauto import TestCase
from sms import SmsTestCommon


class TestSmsIncomingGetMessage(TestCase, SmsTestCommon):
    def tearDown(self):
        self.marionette.execute_script("""
            SpecialPowers.removePermission("sms", document);
            SpecialPowers.setBoolPref("dom.sms.enabled", false);
        """)
        TestCase.tearDown(self)

    def test_sms_incoming_get_message(self):
        # have user send sms to the Firefox OS device, verify body
        self.user_guided_incoming_sms()

        # test mozMobileMessage.getMessage with valid id
        sms_to_get = self.in_sms['id']
        error_message = "mozMobileMessage.getMessage should have found the SMS message"
        self.get_message(sms_to_get, True, error_message)

        # verify correct message was found; just check id and body text
        event_sms = self.marionette.execute_script("return window.wrappedJSObject.event_sms")
        self.assertEqual(event_sms['id'], sms_to_get, "MozMobileMessage.id of found SMS should match the received SMS")
        self.assertEqual(event_sms['body'], self.in_sms['body'], "Message body of the found SMS should match the received SMS")

        # test mozMobileMessage.getMessage with invalid message object; should fail
        sms_to_get = self.in_sms['id'] + 999 # no chance of receiving 999 more SMS between test cases
        error_message = "mozMobileMessage.getMessage should NOT have found the SMS message"
        self.get_message(sms_to_get, False, error_message)
