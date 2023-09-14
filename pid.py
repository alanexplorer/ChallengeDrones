class PIDController:
	def __init__(self, kp, ki, kd):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.prev_error = 0
		self.integral = 0

	def update(self, error):
		p = self.kp * error

		self.integral += error
		i = self.ki * self.integral

		d = self.kd * (error - self.prev_error)
		self.prev_error = error

		control_output = p + i + d

		return control_output # Usado em align
