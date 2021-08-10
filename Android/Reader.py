import sqlite3
import discord
#from datetime import date as _date



class UserList():
	def __init__(self,c):
		self.List=list()
		c.execute('''
		SELECT DISTINCT user 
		FROM _TASK_INST
		''')
		l=c.fetchall()
		for i in l:#list of unique user
			self.List.append(User(i))
			pass
			
		for i in self.List:#liat of task per user
			q='SELECT * FROM _TASK_INST WHERE user = {}'.format(i.Name)
			w=q.split(',')
			w[0]+=')'
#			print(w[0])
			c.execute(w[0])
			for a in c.fetchall():
				i.Task_Que.append(Task(a,i))
			pass
		pass
		
		
class User:
	def __init__(self):
		self.Task_Que =list()
		self.Name='Undefined'
		self.key=-1
	pass
	def __init__(self,val):
		self.Task_Que =list()
		self.Name=str(val)
		self.key=-1
	pass
	
	def Update_que(self,c):
		c.execute('SELECT * FROM _TASK_INST WHERE name = (?)',(self.Name,))
		for b in c.fetchall():
			d=Date(b[1])
			
		pass
	
		
class Date:
	def __init__(self):
		self.Month=0
		self.Year=0
		self.Date=0
	pass
	def __init__(self,val):
		
		cl=type(val)
		
		if cl==Date:
			self.Month=val.Month
			self.Year=val.Year
			self.Date=val.Date
		else:
				if(cl==str):
					text=val.split('-')
				 #ifstring
				else:
					if cl == list:
						text=val
					pass #iflist
				
				self.Month=text[1]
				self.Year=text[0]
				self.Date=text[2]
	pass #if not copy
	pass #func
	def SetDate(self,val):
		#xxxx-mm-dd
		self=Date(val)
		pass
	@staticmethod
	def today():
		return Date(str(_date.today()))
	
	def ToString(self):
		text='Year:'+self.Year
		text+='\n'
		text+='Month:'+self.Month
		text+='\n'
		text+='Date:'+self.Date
		text+='\n'
		return text
#OPERATOR OVERLOADING	
	def __gr__(self,val):
		v=Date(val)
		if self.Year>v.Year:
			return True
		pass
		if self.Month>v.Month:
			return True
		pass
		if self.Date>v.Date:
			return True
		pass
		return False
		
	def __lt__(self,val):
		v=Date(val)
		if self.Year<v.Year:
			return True
		pass
		if self.Month<v.Month:
			return True
		pass
		if self.Date<v.Date:
			return True
		pass
		return False
		
	def __eq__(self,val):
		v=Date(val)
		if self.Year==v.Year:			
			if self.Month==v.Month:
				if self.Date==v.Date:
					return True
		pass
		return False
		
		
class Task:
	def __init__(self):
		self.Name = 'undefined'
		self.Date = Date()
		self.User=User()
		self.Description='undefined'
		self.IsCompleted=False
		pass
	def __init__(self,val,user):
		self.Name=val[0]
		self.User=user
		self.Date=Date(val[1])
		self.Description=val[2]
		self.IsCompleted =val[4]
		pass
	@staticmethod
	def GetAll(c):
		c.execute('''
		SELECT * FROM _TASK_INST
		''')
		return c.fetchall()
#	def CompareTime(year,month,date):
print(Date.today().ToString())

