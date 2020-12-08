from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

feedback = []
class Signin :						#Sign in to AIMS
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def enter_site(self) :			#Entering AIMS from Home page
		self.driver = webdriver.Chrome()
		self.driver.get("https://iith.ac.in/")
		self.driver.maximize_window()
		time.sleep(2)

	def scroll(self) :			#Scrolling till down the page
		scroll_pause = 2
		last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
		while True:
			self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			time.sleep(scroll_pause)
			new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

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

	def feedback_fn(self) :										#Submits the Feedback in AIMS Portal
		self.driver.find_element_by_xpath("//*[@id='red']/li/ul/li[5]/div").click()
		time.sleep(2)
		self.driver.find_element_by_xpath("//*[@id='red']/li/ul/li[5]/ul/li[4]/span").click()
		time.sleep(5)
		feedback_buttons = self.driver.find_elements_by_class_name('fb_status_change_icon')
		for button in feedback_buttons :
			link = button.get_attribute('href')
			array = link.split('/')
			array[-2] = 'courseFeedback'
			code = link.split('/')[-1]
			final=''
			for x in array:
				final += x + '/'
			code = link.split('/')[-1]
			link = final
			int_code = int(code)+802
			final_link = link[:-5] + str(int_code) +'/'+ link[-5:-1]
			feedback.append(final_link)
			time.sleep(1)
		for x in feedback :
			self.driver.get(x)
			self.driver.find_element_by_id('fbRemarks').send_keys('.')
			i = 1
			while(i < 21) :		# Choosing N/A
				id_num = 'na_'+str(i)
				self.driver.find_element_by_id(id_num).click()
				time.sleep(0.5)
				if i==8 :
					scroll_pause = 2
					last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
					while True:
						self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
						time.sleep(scroll_pause)
						new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
						if new_height == last_height:
							break
					last_height = new_height
				i+=1
			self.driver.find_element_by_id('savefb').click()
			time.sleep(3)




def initiate() :				# Initiate
	username = input("Enter your Login Id : ")
	password = input("Enter your password : ")
	obj = Signin(username, password)
	obj.enter_site()
	obj.scroll()
	obj.go_to_aims()
	obj.login()
	obj.feedback_fn()
	print("Yayyyyy Course Feedback Submitted")

initiate()