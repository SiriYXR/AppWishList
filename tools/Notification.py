# -*- coding:utf-8 -*-
"""
@author:SiriYang
@file: Notification.py
@time: 2020.2.1 20:11
"""

import reminders
from datetime import datetime,timedelta

class Notification (object):
	
	def __init__(self,calendar):
		self.calendar=calendar
		
	def addNotice(self,info):
		notice=reminders.Reminder(self.getCalendar())
		notice.title=info
		due=datetime.now()+timedelta(seconds=1)
		notice.due_date=due
		alarm=reminders.Alarm()
		alarm.date=due
		notice.alarms=[alarm]
		
		notice.save()
		
	def getCalendar(self):
		
		c=None
		cs=reminders.get_all_calendars()
		
		for i in cs:
			if i.title == self.calendar:
				c=i
				break
		else:
			c=reminders.Calendar()
			c.title=self.calendar
			c.save()	
		
		return c
		
if __name__ == "__main__":
	n=Notification("AppWishList")
	n.addNotice("hello world!")
