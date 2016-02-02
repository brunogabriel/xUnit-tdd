# Example from TDD: Kent Beck book
class TestResult:
	"""Class used to count when tests pass or not 
	"""
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0

	def testStarted(self):
		self.runCount = self.runCount + 1

	def testFailed(self):
		self.errorCount = self.errorCount + 1

	def summary(self):
		return "%d run, %d failed" % (self.runCount, self.errorCount)



class TestCase:
	"""Class used to call a method and start a test
	"""
	def __init__(self, name):
		self.name = name

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def run(self, result):
		result.testStarted()
		self.setUp()
		try:
			# find a method by your name
			method = getattr(self, self.name)
			method()
		except Exception as e:
			print str(e)
			result.testFailed()
		self.tearDown()



class WasRun(TestCase):
	"""Class from TestCase that executes call run
	"""
	def __init__(self, name):
		TestCase.__init__(self, name)

	def setUp(self):
		self.log = "setUp "

	def testMethod(self):
		self.log = self.log + "testMethod "

	def testBrokenMethod(self):
		raise Exception

	def tearDown(self):
		self.log = self.log + "tearDown "



class TestCaseTest(TestCase):
	"""Class to Test TestCase ;P
	"""
	def setUp(self):
		self.result = TestResult()

	def testResult(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("1 run, 0 failed" == self.result.summary())

	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("setUp testMethod tearDown " == test.log)

	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert("1 run, 1 failed" == self.result.summary())

	def testFailedResultFormatting(self):
		self.result.testStarted()
		self.result.testFailed()
		assert("1 run, 1 failed" == self.result.summary())

	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun("testMethod"))
		suite.add(WasRun("testBrokenMethod"))
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())



class TestSuite:
	"""Class to register a TestCase Collection and execute all
	"""
	def __init__(self):
		# empty TestCases
		self.tests = []

	def add(self, test):
		if test:
			self.tests.append(test)

	def run(self, result):
		for test in self.tests:
			test.run(result)



# Let's run our tests
suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testSuite"))
result = TestResult()
suite.run(result)
print result.summary()
