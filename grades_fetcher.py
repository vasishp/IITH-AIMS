from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class Signin :						#Sign in to AIMS
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def enter_site(self) :			#Entering AIMS from Home page
		self.driver = webdriver.Chrome()
		self.driver.get("https://iith.ac.in/")
		time.sleep(2)

	def scroll(self) :			#Scrolling till down the page
		scroll_pause = 2
		last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
		while True:
			self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			time.sleep(scroll_pause)
			new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
			if new_height == last_height:
				print("\nScrolling Finished!\n")
				break
			last_height = new_height
			print("\nScrolling")

	def go_to_aims(self) :		#Opening AIMS Page
		self.driver.find_element_by_xpath("//div[@id='site-content']/footer/div/div/div/div/ul/li[1]/a").click()
		time.sleep(3)

	def login(self) :			#Login to AIMS Portal
		self.driver.switch_to.window(self.driver.window_handles[1])
		bot = self.driver.find_elements_by_tag_name('div')
		for x in bot :
			if x.get_attribute('class') == 'email-div row' :
				x.find_element_by_xpath("//input[2][@type='email']").send_keys(self.username)
			elif x.get_attribute('class') == 'passwd-div row' :
				x.find_element_by_xpath("//input[@type='password']").send_keys(self.password)
			elif x.get_attribute('class') == 'filditem' :
				captcha_sen = x.find_element_by_xpath("//div[3]/div/img").get_attribute('src')
				captcha = captcha_sen.split('/')
				x.find_element_by_xpath("//div[5]/div/input[2][@type='text']").send_keys(captcha[-1])
		self.driver.find_element_by_id('login').click()	
		time.sleep(3)
		self.driver.find_element_by_id('appCaptchaLoginImg')
		self.driver.save_screenshot('screenshot.png')
		self.driver.find_element_by_id('appCaptchaLoginImg')
		time.sleep(15)										# Need to enter captcha in 15 seconds
		self.driver.find_element_by_id("submit").click()
		time.sleep(3)

	def grades(self) :										#Fetches the grades of the latest semester
		self.driver.find_element_by_xpath("//*[@id='red']/li/ul/li[5]/div").click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//*[@id='red']/li/ul/li[5]/ul/li[4]/span").click()
		time.sleep(10)
		course_list = self.driver.find_element_by_xpath("//*[@id='courseHistoryUI']/ul[2]")
		each_course = course_list.find_elements_by_tag_name('li')
		for course in each_course :
			if (course.get_attribute('class')=='hierarchyLi dataLi tab_body_bg') :
				i=-1
				for x in course.find_elements_by_tag_name('span') :
					i+=1
					if(x.get_attribute('class').split(' ')[-1]=='col'):
						if(i==3 or i==4) :
							continue 
						elif (i==8):
							print("------")
							continue
						print(x.text)


def initiate() :				# Initiate
	username = input("Enter your Login Id : ")
	password = input("Enter your password : ")
	obj = Signin(username, password)
	obj.enter_site()
	obj.scroll()
	obj.go_to_aims()
	obj.login()
	obj.grades()

initiate()