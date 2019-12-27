#!/usr/bin/env python3

from time import sleep
from alert import Alert
from alert_recipients import emails, sms_numbers
from sound import Sound

a = Alert()
s = Sound(default_recording_time=5)

print("Program Start")
s.StartRecording()
s.GetRecording() # Wait for the first one to finish
while True:
    # Start the new recording while we process the old one
    s.StartRecording()
    if s.PatternMatched() is True:
        print("Pattern Matched!")
        a.Email(emails)
        # Need some kind of cooloff here otherwise we'll spam emails
        # Simplest thing is just to sleep after triggering
        sleep(60*60)  # 1 hour
        print("Waking from sleep...")
        s.GetRecording()  # To ensure the other one has finished
        s.StartRecording()  # The old one is stale
    s.GetRecording()
    